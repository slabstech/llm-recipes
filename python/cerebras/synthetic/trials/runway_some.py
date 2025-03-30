from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFilter
import io
import torch
import numpy as np
from diffusers import StableDiffusionInpaintPipeline
import cv2

# Initialize FastAPI app
app = FastAPI()

# Load the pre-trained inpainting model (Stable Diffusion)
model_id = "runwayml/stable-diffusion-inpainting"
device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    pipe = StableDiffusionInpaintPipeline.from_pretrained(model_id)
    pipe.to(device)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "InstructPix2Pix API is running. Use POST /inpaint/, /inpaint-with-reference/, or /fit-image-to-mask/ to edit images."}

# Helper functions
def prepare_guided_image(original_image: Image, reference_image: Image, mask_image: Image) -> Image:
    original_array = np.array(original_image)
    reference_array = np.array(reference_image)
    mask_array = np.array(mask_image) / 255.0
    mask_array = mask_array[:, :, np.newaxis]
    blended_array = original_array * (1 - mask_array) + reference_array * mask_array
    return Image.fromarray(blended_array.astype(np.uint8))

def soften_mask(mask_image: Image, softness: int = 5) -> Image:
    from PIL import ImageFilter
    return mask_image.filter(ImageFilter.GaussianBlur(radius=softness))

def generate_rectangular_mask(image_size: tuple, x1: int = 100, y1: int = 100, x2: int = 200, y2: int = 200) -> Image:
    mask = Image.new("L", image_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([x1, y1, x2, y2], fill=255)
    return mask

def segment_tank(tank_image: Image) -> tuple[Image, Image]:
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

async def apply_camouflage_to_tank(tank_image: Image) -> Image:
    segmented_tank, tank_mask = segment_tank(tank_image)
    segmented_tank.save("segmented_tank.png")
    tank_mask.save("tank_mask.png")
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
    camouflaged_tank_image = Image.fromarray(camouflaged_tank_rgba, mode="RGBA")
    camouflaged_tank_image.save("camouflaged_tank.png")
    return camouflaged_tank_image

def fit_image_to_mask(original_image: Image, reference_image: Image, mask_x1: int, mask_y1: int, mask_x2: int, mask_y2: int) -> tuple:
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
@app.post("/inpaint/")
async def inpaint_image(
    image: UploadFile = File(...),
    mask: UploadFile = File(...),
    prompt: str = "Fill the masked area with appropriate content."
):
    try:
        image_bytes = await image.read()
        mask_bytes = await mask.read()
        original_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        mask_image = Image.open(io.BytesIO(mask_bytes)).convert("L")
        if original_image.size != mask_image.size:
            raise HTTPException(status_code=400, detail="Image and mask dimensions must match.")
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
        raise HTTPException(status_code=500, detail=f"Error during inpainting: {e}")

@app.post("/inpaint-with-reference/")
async def inpaint_with_reference(
    image: UploadFile = File(...),
    reference_image: UploadFile = File(...),
    prompt: str = "Integrate the reference content naturally into the masked area, matching style and lighting.",
    mask_x1: int = 100,
    mask_y1: int = 100,
    mask_x2: int = 200,
    mask_y2: int = 200
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
        raise HTTPException(status_code=500, detail=f"Error during natural inpainting: {e}")

@app.post("/fit-image-to-mask/")
async def fit_image_to_mask_endpoint(
    image: UploadFile = File(...),
    reference_image: UploadFile = File(...),
    mask_x1: int = 200,
    mask_y1: int = 200,
    mask_x2: int = 500,
    mask_y2: int = 500
):
    try:
        image_bytes = await image.read()
        reference_bytes = await reference_image.read()
        original_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        reference_image = Image.open(io.BytesIO(reference_bytes)).convert("RGB")
        camouflaged_tank = await apply_camouflage_to_tank(reference_image)
        guided_image, mask_image = fit_image_to_mask(original_image, camouflaged_tank, mask_x1, mask_y1, mask_x2, mask_y2)
        guided_image.save("guided_image_before_blending.png")
        softened_mask = soften_mask(mask_image, softness=2)
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

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)