from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw
import io
import torch
import numpy as np
from diffusers import StableDiffusionInpaintPipeline

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
    """
    Root endpoint for basic health check.
    """
    return {"message": "InstructPix2Pix API is running. Use POST /inpaint/, /inpaint-with-reference/, or /fit-image-to-mask/ to edit images."}

# Helper functions
def prepare_guided_image(original_image: Image, reference_image: Image, mask_image: Image) -> Image:
    """
    Prepare an initial image by softly blending the reference image into the masked area.
    - Areas to keep (black in mask, 0) remain fully from the original image.
    - Areas to inpaint (white in mask, 255) take content from the reference image with soft blending.
    """
    original_array = np.array(original_image)
    reference_array = np.array(reference_image)
    mask_array = np.array(mask_image) / 255.0
    mask_array = mask_array[:, :, np.newaxis]
    blended_array = original_array * (1 - mask_array) + reference_array * mask_array
    return Image.fromarray(blended_array.astype(np.uint8))

def soften_mask(mask_image: Image, softness: int = 5) -> Image:
    """
    Soften the edges of the mask for smoother transitions.
    """
    from PIL import ImageFilter
    return mask_image.filter(ImageFilter.GaussianBlur(radius=softness))

def generate_rectangular_mask(image_size: tuple, x1: int = 100, y1: int = 100, x2: int = 200, y2: int = 200) -> Image:
    """
    Generate a rectangular mask matching the image dimensions.
    - Black (0) for areas to keep, white (255) for areas to inpaint.
    """
    mask = Image.new("L", image_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([x1, y1, x2, y2], fill=255)
    return mask

def fit_image_to_mask(original_image: Image, reference_image: Image, mask_x1: int, mask_y1: int, mask_x2: int, mask_y2: int) -> tuple:
    """
    Fit the reference image into the masked region of the original image.
    
    Args:
        original_image (Image): The original image (RGB).
        reference_image (Image): The image to fit into the masked region (RGB).
        mask_x1, mask_y1, mask_x2, mask_y2 (int): Coordinates of the masked region.
    
    Returns:
        tuple: (guided_image, mask_image) - The image with the fitted reference and the corresponding mask.
    """
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
    guided_image = original_image.copy()
    paste_x = mask_x1 + (mask_width - new_width) // 2
    paste_y = mask_y1 + (mask_height - new_height) // 2
    guided_image.paste(reference_image_resized, (paste_x, paste_y))
    mask_image = generate_rectangular_mask(original_image.size, mask_x1, mask_y1, mask_x2, mask_y2)
    return guided_image, mask_image

def create_tank_mask(tank_image: Image) -> Image:
    """
    Create a mask for the tank by assuming the background is mostly uniform (e.g., white or transparent).
    This is a simplified approach; for better results, use a segmentation model.
    """
    tank_array = np.array(tank_image.convert("RGBA"))  # Use RGBA to handle transparency
    # Assume the background is white or transparent (simplified)
    # Create a mask where the tank is (non-background pixels)
    mask = np.zeros((tank_image.height, tank_image.width), dtype=np.uint8)
    # If the alpha channel is 0 (transparent) or the pixel is white, mark it as background (0)
    for i in range(tank_image.height):
        for j in range(tank_image.width):
            r, g, b, a = tank_array[i, j]
            if a == 0 or (r > 200 and g > 200 and b > 200):  # Transparent or white
                mask[i, j] = 0  # Background
            else:
                mask[i, j] = 255  # Tank
    return Image.fromarray(mask, mode="L")

async def apply_camouflage_to_tank(tank_image: Image) -> Image:
    """
    Apply a grassy camouflage pattern to the tank using Stable Diffusion inpainting.
    """
    # Create a mask for the tank
    tank_mask = create_tank_mask(tank_image)

    # Debug: Save the mask to verify
    tank_mask.save("tank_mask.png")

    # Apply camouflage using inpainting
    camouflaged_tank = pipe(
        prompt="Apply a grassy camouflage pattern with shades of green and brown to the tank, preserving its structure.",
        image=tank_image.convert("RGB"),
        mask_image=tank_mask,
        strength=0.4,  # Moderate strength to apply camouflage without overwriting the tank
        guidance_scale=8.0,
        num_inference_steps=50,
        negative_prompt="rock, stone, boat, unrelated objects"
    ).images[0]

    # Debug: Save the camouflaged tank to verify
    camouflaged_tank.save("camouflaged_tank.png")

    return camouflaged_tank

# Endpoints
@app.post("/inpaint/")
async def inpaint_image(
    image: UploadFile = File(...),
    mask: UploadFile = File(...),
    prompt: str = "Fill the masked area with appropriate content."
):
    """
    Endpoint for image inpainting using a text prompt and an uploaded mask.
    - `image`: Original image file (PNG/JPG).
    - `mask`: Mask file indicating areas to inpaint (white for masked areas, black for unmasked).
    - `prompt`: Text prompt describing the desired output.
    
    Returns:
    - The inpainted image as a PNG file.
    """
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
    """
    Endpoint for replacing masked areas with reference image content, refined to look natural, using an autogenerated mask.
    """
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
    """
    Endpoint for fitting a reference image (tank) into a masked region of the original image (field),
    with a two-step approach: first apply camouflage to the tank, then blend it into the scene.
    """
    try:
        # Load the uploaded images
        image_bytes = await image.read()
        reference_bytes = await reference_image.read()
        original_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        reference_image = Image.open(io.BytesIO(reference_bytes)).convert("RGB")

        # Step 1: Apply camouflage to the tank
        camouflaged_tank = await apply_camouflage_to_tank(reference_image)

        # Step 2: Fit the camouflaged tank into the field and blend
        guided_image, mask_image = fit_image_to_mask(original_image, camouflaged_tank, mask_x1, mask_y1, mask_x2, mask_y2)

        # Debug: Save the guided_image to verify placement
        guided_image.save("guided_image_before_blending.png")

        # Soften the mask for smoother transitions
        softened_mask = soften_mask(mask_image, softness=2)

        # Blend the camouflaged tank into the field
        result = pipe(
            prompt="Blend the camouflaged tank into the field with trees, matching the style, lighting, and surroundings.",
            image=guided_image,
            mask_image=softened_mask,
            strength=0.3,  # Lower strength to focus on blending, not modifying the tank
            guidance_scale=7.5,
            num_inference_steps=50,
            negative_prompt="rock, stone, boat, unrelated objects"
        ).images[0]

        # Convert result to bytes for response
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