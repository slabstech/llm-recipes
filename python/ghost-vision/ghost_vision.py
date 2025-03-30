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
from typing import Optional

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

# Image processing helper functions (unchanged, included for completeness)
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

@app.post("/detect-json/")
async def detect_json(file: UploadFile = File(...), text_query: str = DEFAULT_TEXT_QUERY):
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
async def segment_image(file: UploadFile = File(...), text_query: str = DEFAULT_TEXT_QUERY):
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
        return StreamingResponse(img_byte_arr, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error segmenting image: {str(e)}")

# Add other endpoints (e.g., /mask-object/, /fit-image-to-mask/) with similar lazy loading patterns as needed

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)