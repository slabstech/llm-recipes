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
    # Calculate mask dimensions
    mask_width = mask_x2 - mask_x1
    mask_height = mask_y2 - mask_y1

    # Ensure mask dimensions are positive
    if mask_width <= 0 or mask_height <= 0:
        raise ValueError("Mask dimensions must be positive")

    # Resize reference image to fit the mask while preserving aspect ratio
    ref_width, ref_height = reference_image.size
    aspect_ratio = ref_width / ref_height

    if mask_width / mask_height > aspect_ratio:
        # Fit to height
        new_height = mask_height
        new_width = int(new_height * aspect_ratio)
    else:
        # Fit to width
        new_width = mask_width
        new_height = int(new_width / aspect_ratio)

    # Resize reference image
    reference_image_resized = reference_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create a copy of the original image to paste the reference image onto
    guided_image = original_image.copy()

    # Calculate position to center the resized image in the mask
    paste_x = mask_x1 + (mask_width - new_width) // 2
    paste_y = mask_y1 + (mask_height - new_height) // 2

    # Paste the resized reference image onto the original image
    guided_image.paste(reference_image_resized, (paste_x, paste_y))

    # Generate the mask for inpainting (white in the pasted region)
    mask_image = generate_rectangular_mask(original_image.size, mask_x1, mask_y1, mask_x2, mask_y2)

    return guided_image, mask_image

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
        # Load the uploaded image and mask
        image_bytes = await image.read()
        mask_bytes = await mask.read()

        original_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        mask_image = Image.open(io.BytesIO(mask_bytes)).convert("L")

        # Ensure dimensions match between image and mask
        if original_image.size != mask_image.size:
            raise HTTPException(status_code=400, detail="Image and mask dimensions must match.")

        # Perform inpainting using the pipeline
        result = pipe(prompt=prompt, image=original_image, mask_image=mask_image).images[0]

        # Convert result to bytes for response
        result_bytes = io.BytesIO()
        result.save(result_bytes, format="PNG")
        result_bytes.seek(0)

        # Return the image as a streaming response
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
    prompt: str = "Blend the fitted image naturally into the scene, matching style and lighting.",
    mask_x1: int = 100,
    mask_y1: int = 100,
    mask_x2: int = 200,
    mask_y2: int = 200
):
    try:
        # Load the uploaded images
        image_bytes = await image.read()
        reference_bytes = await reference_image.read()
        original_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        reference_image = Image.open(io.BytesIO(reference_bytes)).convert("RGB")

        # Fit the reference image into the masked region (await the async function)
        guided_image, mask_image = await fit_image_to_mask(original_image, reference_image, mask_x1, mask_y1, mask_x2, mask_y2)

        # Soften the mask for smoother transitions
        softened_mask = soften_mask(mask_image, softness=5)

        # Perform inpainting to blend the fitted image naturally
        result = pipe(
            prompt=prompt,
            image=guided_image,
            mask_image=softened_mask,
            strength=0.75,
            guidance_scale=7.5
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