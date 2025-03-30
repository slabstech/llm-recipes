from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse, Response
import io
import math
from PIL import Image, ImageOps, ImageDraw, ImageFilter
import torch
import numpy as np
from diffusers import (
    StableDiffusionInstructPix2PixPipeline,
    StableDiffusionInpaintPipeline,
    StableDiffusionXLPipeline,
    UNet2DConditionModel,
    EulerDiscreteScheduler,
)
from huggingface_hub import hf_hub_download, login
from safetensors.torch import load_file
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
from sam2.sam2_image_predictor import SAM2ImagePredictor
import cv2
import os
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI()

# Device configuration
device = "cuda" if torch.cuda.is_available() else "cpu"

# Model variables (initially None, loaded lazily)
pipe_edit = None  # InstructPix2Pix
pipe_inpaint = None  # Stable Diffusion Inpainting
pipe_generate = None  # Stable Diffusion XL
pipe_runway = None  # Runway Inpainting
dino_processor = None  # Grounding DINO processor
dino_model = None  # Grounding DINO model
sam_predictor = None  # SAM 2 predictor

# Default configuration values
DEFAULT_STEPS = 50
DEFAULT_TEXT_CFG = 7.5
DEFAULT_IMAGE_CFG = 1.5
DEFAULT_SEED = 1371
DEFAULT_TEXT_QUERY = "a tank."
HF_TOKEN = os.getenv("HF_TOKEN")

# Helper functions for lazy loading
def load_instruct_pix2pix() -> StableDiffusionInstructPix2PixPipeline:
    global pipe_edit
    if pipe_edit is None:
        model_id = "timbrooks/instruct-pix2pix"
        pipe_edit = StableDiffusionInstructPix2PixPipeline.from_pretrained(
            model_id, torch_dtype=torch.float16, safety_checker=None
        ).to(device)
    return pipe_edit

def load_inpaint_pipeline() -> StableDiffusionInpaintPipeline:
    global pipe_inpaint
    if pipe_inpaint is None:
        inpaint_model_id = "stabilityai/stable-diffusion-2-inpainting"
        pipe_inpaint = StableDiffusionInpaintPipeline.from_pretrained(
            inpaint_model_id, torch_dtype=torch.float16, safety_checker=None
        ).to(device)
    return pipe_inpaint

def load_generate_pipeline() -> StableDiffusionXLPipeline:
    global pipe_generate
    if pipe_generate is None:
        try:
            if HF_TOKEN:
                login(token=HF_TOKEN)
            base = "stabilityai/stable-diffusion-xl-base-1.0"
            repo = "ByteDance/SDXL-Lightning"
            ckpt = "sdxl_lightning_4step_unet.safetensors"
            unet = UNet2DConditionModel.from_config(base, subfolder="unet").to(device, torch.float16)
            unet.load_state_dict(load_file(hf_hub_download(repo, ckpt), device=device))
            pipe_generate = StableDiffusionXLPipeline.from_pretrained(
                base, unet=unet, torch_dtype=torch.float16, variant="fp16"
            ).to(device)
            pipe_generate.scheduler = EulerDiscreteScheduler.from_config(
                pipe_generate.scheduler.config, timestep_spacing="trailing"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load generate pipeline: {str(e)}")
    return pipe_generate

def load_runway_inpaint() -> StableDiffusionInpaintPipeline:
    global pipe_runway
    if pipe_runway is None:
        model_id_runway = "runwayml/stable-diffusion-inpainting"
        pipe_runway = StableDiffusionInpaintPipeline.from_pretrained(model_id_runway).to(device)
    return pipe_runway

def load_dino() -> tuple[AutoProcessor, AutoModelForZeroShotObjectDetection]:
    global dino_processor, dino_model
    if dino_processor is None or dino_model is None:
        dino_model_id = "IDEA-Research/grounding-dino-base"
        dino_processor = AutoProcessor.from_pretrained(dino_model_id)
        dino_model = AutoModelForZeroShotObjectDetection.from_pretrained(dino_model_id).to(device)
    return dino_processor, dino_model

def load_sam() -> SAM2ImagePredictor:
    global sam_predictor
    if sam_predictor is None:
        sam_predictor = SAM2ImagePredictor.from_pretrained("facebook/sam2-hiera-tiny")
        sam_predictor.model.to(device)
    return sam_predictor

# Image processing helper functions
def process_image_with_dino(image: Image.Image, text_query: str = DEFAULT_TEXT_QUERY):
    processor, model = load_dino()
    inputs = processor(images=image, text=text_query, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    results = processor.post_process_grounded_object_detection(
        outputs, inputs.input_ids, threshold=0.4, text_threshold=0.3, target_sizes=[image.size[::-1]]
    )
    return results[0]

def segment_with_sam(image: Image.Image, boxes: list):
    predictor = load_sam()
    image_np = np.array(image)
    predictor.set_image(image_np)
    if not boxes:
        return np.zeros(image_np.shape[:2], dtype=bool)
    boxes_tensor = torch.tensor(
        [[box["x_min"], box["y_min"], box["x_max"], box["y_max"]] for box in boxes],
        dtype=torch.float32
    ).to(device)
    masks, _, _ = predictor.predict(point_coords=None, point_labels=None, box=boxes_tensor, multimask_output=False)
    return masks[0]

def create_background_mask(image_np: np.ndarray, mask: np.ndarray) -> np.ndarray:
    mask_inv = np.logical_not(mask).astype(np.uint8) * 255
    mask_rgb = cv2.cvtColor(mask_inv, cv2.COLOR_GRAY2RGB)
    return mask_rgb

def create_object_mask(image_np: np.ndarray, mask: np.ndarray) -> np.ndarray:
    mask_rgb = cv2.cvtColor(mask.astype(np.uint8) * 255, cv2.COLOR_GRAY2RGB)
    return mask_rgb

def process_image(input_image: Image.Image, instruction: str, steps: int, text_cfg_scale: float, image_cfg_scale: float, seed: int):
    width, height = input_image.size
    factor = 512 / max(width, height)
    factor = math.ceil(min(width, height) * factor / 64) * 64 / min(width, height)
    width = int((width * factor) // 64) * 64
    height = int((height * factor) // 64) * 64
    input_image = ImageOps.fit(input_image, (width, height), method=Image.Resampling.LANCZOS)
    if not instruction:
        return input_image
    generator = torch.manual_seed(seed)
    pipe = load_instruct_pix2pix()
    edited_image = pipe(
        instruction,
        image=input_image,
        guidance_scale=text_cfg_scale,
        image_guidance_scale=image_cfg_scale,
        num_inference_steps=steps,
        generator=generator,
    ).images[0]
    return edited_image

def prepare_guided_image(original_image: Image.Image, reference_image: Image.Image, mask_image: Image.Image) -> Image.Image:
    original_array = np.array(original_image)
    reference_array = np.array(reference_image)
    mask_array = np.array(mask_image) / 255.0
    mask_array = mask_array[:, :, np.newaxis]
    blended_array = original_array * (1 - mask_array) + reference_array * mask_array
    return Image.fromarray(blended_array.astype(np.uint8))

def soften_mask(mask_image: Image.Image, softness: int = 5) -> Image.Image:
    return mask_image.filter(ImageFilter.GaussianBlur(radius=softness))

def generate_rectangular_mask(image_size: tuple, x1: int = 100, y1: int = 100, x2: int = 200, y2: int = 200) -> Image.Image:
    mask = Image.new("L", image_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([x1, y1, x2, y2], fill=255)
    return mask

def segment_tank(tank_image: Image.Image) -> tuple[Image.Image, Image.Image]:
    tank_array = np.array(tank_image.convert("RGB"))
    tank_array = cv2.cvtColor(tank_array, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(tank_array, cv2.COLOR_BGR2HSV)
    lower_snow = np.array([0, 0, 180])
    upper_snow = np.array([180, 50, 255])
    snow_mask = cv2.inRange(hsv, lower_snow, upper_snow)
    tank_mask = cv2.bitwise_not(snow_mask)
    kernel = np.ones((5, 5), np.uint8)
    tank_mask = cv2.erode(tank_mask, kernel, iterations=1)
    tank_mask = cv2.dilate(tank_mask, kernel, iterations=1)
    tank_mask_image = Image.fromarray(tank_mask, mode="L")
    tank_array_rgb = np.array(tank_image.convert("RGB"))
    mask_array = tank_mask / 255.0
    mask_array = mask_array[:, :, np.newaxis]
    segmented_tank = (tank_array_rgb * mask_array).astype(np.uint8)
    alpha = tank_mask
    segmented_tank_rgba = np.zeros((tank_image.height, tank_image.width, 4), dtype=np.uint8)
    segmented_tank_rgba[:, :, :3] = segmented_tank
    segmented_tank_rgba[:, :, 3] = alpha
    segmented_tank_image = Image.fromarray(segmented_tank_rgba, mode="RGBA")
    return segmented_tank_image, tank_mask_image

async def apply_camouflage_to_tank(tank_image: Image.Image) -> Image.Image:
    segmented_tank, tank_mask = segment_tank(tank_image)
    pipe = load_runway_inpaint()
    camouflaged_tank = pipe(
        prompt="Apply a grassy camouflage pattern with shades of green and brown to the tank, preserving its structure.",
        image=segmented_tank.convert("RGB"),
        mask_image=tank_mask,
        strength=0.5,
        guidance_scale=8.0,
        num_inference_steps=50,
        negative_prompt="snow, ice, rock, stone, boat, unrelated objects"
    ).images[0]
    camouflaged_tank_rgba = np.zeros((camouflaged_tank.height, camouflaged_tank.width, 4), dtype=np.uint8)
    camouflaged_tank_rgba[:, :, :3] = np.array(camouflaged_tank)
    camouflaged_tank_rgba[:, :, 3] = np.array(tank_mask)
    return Image.fromarray(camouflaged_tank_rgba, mode="RGBA")

def fit_image_to_mask(original_image: Image.Image, reference_image: Image.Image, mask_x1: int, mask_y1: int, mask_x2: int, mask_y2: int) -> tuple:
    mask_width = mask_x2 - mask_x1
    mask_height = mask_y2 - mask_y1
    if mask_width <= 0 or mask_height <= 0:
        raise ValueError("Mask dimensions must be positive")
    ref_width, ref_height = reference_image.size
    aspect_ratio = ref_width / ref_height
    if mask_width / mask_height > aspect_ratio:
        new_height = mask_height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = mask_width
        new_height = int(new_width / aspect_ratio)
    reference_image_resized = reference_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    guided_image = original_image.copy().convert("RGB")
    paste_x = mask_x1 + (mask_width - new_width) // 2
    paste_y = mask_y1 + (mask_height - new_height) // 2
    guided_image.paste(reference_image_resized, (paste_x, paste_y), reference_image_resized)
    mask_image = generate_rectangular_mask(original_image.size, mask_x1, mask_y1, mask_x2, mask_y2)
    return guided_image, mask_image

# Endpoints
@app.get("/generate")
async def generate_image(prompt: str):
    try:
        pipe = load_generate_pipeline()
        image = pipe(prompt, num_inference_steps=4, guidance_scale=0).images[0]
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return Response(content=buffer.getvalue(), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/edit-image/")
async def edit_image(
    file: UploadFile = File(...),
    instruction: str = Form(...),
    steps: int = Form(default=DEFAULT_STEPS),
    text_cfg_scale: float = Form(default=DEFAULT_TEXT_CFG),
    image_cfg_scale: float = Form(default=DEFAULT_IMAGE_CFG),
    seed: int = Form(default=DEFAULT_SEED)
):
    try:
        image_data = await file.read()
        input_image = Image.open(io.BytesIO(image_data)).convert("RGB")
        edited_image = process_image(input_image, instruction, steps, text_cfg_scale, image_cfg_scale, seed)
        img_byte_arr = io.BytesIO()
        edited_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        return StreamingResponse(img_byte_arr, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error editing image: {str(e)}")

@app.post("/inpaint/")
async def inpaint_image(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    mask_coordinates: str = Form(...),
    steps: int = Form(default=DEFAULT_STEPS),
    guidance_scale: float = Form(default=7.5),
    seed: int = Form(default=DEFAULT_SEED)
):
    try:
        image_data = await file.read()
        input_image = Image.open(io.BytesIO(image_data)).convert("RGB")
        width, height = input_image.size
        factor = 512 / max(width, height)
        factor = math.ceil(min(width, height) * factor / 8) * 8 / min(width, height)
        width = int((width * factor) // 8) * 8
        height = int((height * factor) // 8) * 8
        input_image = ImageOps.fit(input_image, (width, height), method=Image.Resampling.LANCZOS)
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        x1, y1, x2, y2 = map(int, mask_coordinates.split(","))
        x1, y1, x2, y2 = int(x1 * factor), int(y1 * factor), int(x2 * factor), int(y2 * factor)
        draw.rectangle([x1, y1, x2, y2], fill=255)
        generator = torch.manual_seed(seed)
        pipe = load_inpaint_pipeline()
        inpainted_image = pipe(
            prompt=prompt,
            image=input_image,
            mask_image=mask,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            generator=generator,
        ).images[0]
        img_byte_arr = io.BytesIO()
        inpainted_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        return StreamingResponse(img_byte_arr, media_type="image/png")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid mask coordinates format. Use 'x1,y1,x2,y2'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inpainting image: {str(e)}")

@app.post("/inpaint-with-mask/")
async def inpaint_with_mask(
    image: UploadFile = File(...),
    mask: UploadFile = File(...),
    prompt: str = Form(default="Fill the masked area with appropriate content.")
):
    try:
        image_bytes = await image.read()
        mask_bytes = await mask.read()
        original_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        mask_image = Image.open(io.BytesIO(mask_bytes)).convert("L")
        if original_image.size != mask_image.size:
            raise HTTPException(status_code=400, detail="Image and mask dimensions must match.")
        pipe = load_runway_inpaint()
        result = pipe(prompt=prompt, image=original_image, mask_image=mask_image).images[0]
        result_bytes = io.BytesIO()
        result.save(result_bytes, format="PNG")
        result_bytes.seek(0)
        return StreamingResponse(
            result_bytes,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=inpainted_image.png"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during inpainting: {str(e)}")

@app.post("/inpaint-with-reference/")
async def inpaint_with_reference(
    image: UploadFile = File(...),
    reference_image: UploadFile = File(...),
    prompt: str = Form(default="Integrate the reference content naturally into the masked area, matching style and lighting."),
    mask_x1: int = Form(default=100),
    mask_y1: int = Form(default=100),
    mask_x2: int = Form(default=200),
    mask_y2: int = Form(default=200)
):
    try:
        image_bytes = await image.read()
        reference_bytes = await reference_image.read()
        original_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        reference_image = Image.open(io.BytesIO(reference_bytes)).convert("RGB")
        if original_image.size != reference_image.size:
            reference_image = reference_image.resize(original_image.size, Image.Resampling.LANCZOS)
        mask_image = generate_rectangular_mask(original_image.size, mask_x1, mask_y1, mask_x2, mask_y2)
        softened_mask = soften_mask(mask_image, softness=5)
        guided_image = prepare_guided_image(original_image, reference_image, softened_mask)
        pipe = load_runway_inpaint()
        result = pipe(
            prompt=prompt,
            image=guided_image,
            mask_image=softened_mask,
            strength=0.75,
            guidance_scale=7.5
        ).images[0]
        result_bytes = io.BytesIO()
        result.save(result_bytes, format="PNG")
        result_bytes.seek(0)
        return StreamingResponse(
            result_bytes,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=natural_inpaint_image.png"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during natural inpainting: {str(e)}")

@app.post("/fit-image-to-mask/")
async def fit_image_to_mask_endpoint(
    image: UploadFile = File(...),
    reference_image: UploadFile = File(...),
    mask_x1: int = Form(default=200),
    mask_y1: int = Form(default=200),
    mask_x2: int = Form(default=500),
    mask_y2: int = Form(default=500)
):
    try:
        image_bytes = await image.read()
        reference_bytes = await reference_image.read()
        original_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        reference_image = Image.open(io.BytesIO(reference_bytes)).convert("RGB")
        camouflaged_tank = await apply_camouflage_to_tank(reference_image)
        guided_image, mask_image = fit_image_to_mask(original_image, camouflaged_tank, mask_x1, mask_y1, mask_x2, mask_y2)
        softened_mask = soften_mask(mask_image, softness=2)
        pipe = load_runway_inpaint()
        result = pipe(
            prompt="Blend the camouflaged tank into the grassy field with trees, ensuring a non-snowy environment, matching the style, lighting, and surroundings.",
            image=guided_image,
            mask_image=softened_mask,
            strength=0.2,
            guidance_scale=7.5,
            num_inference_steps=50,
            negative_prompt="snow, ice, rock, stone, boat, unrelated objects"
        ).images[0]
        result_bytes = io.BytesIO()
        result.save(result_bytes, format="PNG")
        result_bytes.seek(0)
        return StreamingResponse(
            result_bytes,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=fitted_image.png"}
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"ValueError in processing: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during fitting and inpainting: {str(e)}")

@app.post("/detect-json/")
async def detect_json(file: UploadFile = File(...), text_query: str = Form(default=DEFAULT_TEXT_QUERY)):
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        results = process_image_with_dino(image, text_query)
        detections = [
            {
                "label": label,
                "score": float(score),
                "box": {"x_min": box[0].item(), "y_min": box[1].item(), "x_max": box[2].item(), "y_max": box[3].item()}
            }
            for box, label, score in zip(results["boxes"].cpu(), results["labels"], results["scores"])
        ]
        return JSONResponse(content={"detections": detections})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/segment-image/")
async def segment_image(file: UploadFile = File(...), text_query: str = Form(default=DEFAULT_TEXT_QUERY)):
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        results = process_image_with_dino(image, text_query)
        boxes = [
            {"x_min": box[0].item(), "y_min": box[1].item(), "x_max": box[2].item(), "y_max": box[3].item()}
            for box in results["boxes"].cpu()
        ]
        mask = segment_with_sam(image, boxes)
        image_np = np.array(image)
        background_mask = create_background_mask(image_np, mask)
        segmented_image = cv2.bitwise_and(image_np, background_mask)
        output_image = Image.fromarray(segmented_image)
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        return StreamingResponse(
            img_byte_arr,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=segmented_image.png"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error segmenting image: {str(e)}")

@app.post("/mask-object/")
async def mask_object(file: UploadFile = File(...), text_query: str = Form(default=DEFAULT_TEXT_QUERY)):
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        results = process_image_with_dino(image, text_query)
        boxes = [
            {"x_min": box[0].item(), "y_min": box[1].item(), "x_max": box[2].item(), "y_max": box[3].item()}
            for box in results["boxes"].cpu()
        ]
        mask = segment_with_sam(image, boxes)
        image_np = np.array(image)
        object_mask = create_object_mask(image_np, mask)
        masked_image = cv2.bitwise_and(image_np, object_mask)
        output_image = Image.fromarray(masked_image)
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        return StreamingResponse(
            img_byte_arr,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=masked_object_image.png"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error masking object: {str(e)}")

@app.get("/")
async def root():
    return {"message": "InstructPix2Pix API is running. Use POST /edit-image/ or /inpaint/ to edit images."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)