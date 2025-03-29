from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
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

@app.get("/")
async def root():
    """
    Root endpoint for basic health check.
    """
    return {"message": "InstructPix2Pix API is running. Use POST /inpaint/ or /inpaint-with-reference/ to edit images."}

def prepare_guided_image(original_image: Image, reference_image: Image, mask_image: Image) -> Image:
    """
    Prepare an initial image by softly blending the reference image into the masked area.
    - Unmasked areas (white in mask, 255) remain fully from the original image.
    - Masked areas (black in mask, 0) take content from the reference image with soft blending.
    
    Args:
        original_image (Image): The original image (RGB).
        reference_image (Image): The reference image to copy from (RGB).
        mask_image (Image): The mask image (grayscale, L mode).
    
    Returns:
        Image: The blended image to guide inpainting.
    """
    # Convert images to numpy arrays
    original_array = np.array(original_image)
    reference_array = np.array(reference_image)
    mask_array = np.array(mask_image) / 255.0  # Normalize to [0, 1] for soft blending

    # Expand mask to RGB channels
    mask_array = mask_array[:, :, np.newaxis]

    # Softly blend: unmasked areas (1) keep original, masked areas (0) use reference
    blended_array = original_array * mask_array + reference_array * (1 - mask_array)
    blended_array = blended_array.astype(np.uint8)

    return Image.fromarray(blended_array)

def soften_mask(mask_image: Image, softness: int = 5) -> Image:
    """
    Soften the edges of the mask for smoother transitions.
    
    Args:
        mask_image (Image): The original mask (grayscale, L mode).
        softness (int): Size of the Gaussian blur kernel for softening edges.
    
    Returns:
        Image: The softened mask.
    """
    from PIL import ImageFilter
    return mask_image.filter(ImageFilter.GaussianBlur(radius=softness))

@app.post("/inpaint/")
async def inpaint_image(
    image: UploadFile = File(...),
    mask: UploadFile = File(...),
    prompt: str = "Fill the masked area with appropriate content."
):
    """
    Endpoint for image inpainting using a text prompt.
    - `image`: Original image file (PNG/JPG).
    - `mask`: Mask file indicating areas to inpaint (black for masked areas, white for unmasked).
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
    mask: UploadFile = File(...),
    reference_image: UploadFile = File(...),
    prompt: str = "Integrate the reference content naturally into the masked area, matching style and lighting."
):
    """
    Endpoint for replacing masked areas with reference image content, refined to look natural.
    - `image`: Original image file (PNG/JPG).
    - `mask`: Mask file (black for areas to replace, white for areas to keep).
    - `reference_image`: Reference image to guide the replacement (PNG/JPG).
    - `prompt`: Text prompt for inpainting refinement.
    
    Returns:
    - The resulting image as a PNG file.
    """
    try:
        # Load the uploaded image, mask, and reference image
        image_bytes = await image.read()
        mask_bytes = await mask.read()
        reference_bytes = await reference_image.read()

        original_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        mask_image = Image.open(io.BytesIO(mask_bytes)).convert("L")
        reference_image = Image.open(io.BytesIO(reference_bytes)).convert("RGB")

        # Ensure dimensions match between image, mask, and reference image
        if original_image.size != mask_image.size:
            raise HTTPException(status_code=400, detail="Image and mask dimensions must match.")
        if original_image.size != reference_image.size:
            reference_image = reference_image.resize(original_image.size, Image.Resampling.LANCZOS)

        # Soften the mask for smoother transitions
        softened_mask = soften_mask(mask_image, softness=5)

        # Prepare the initial guided image by blending reference content into the masked area
        guided_image = prepare_guided_image(original_image, reference_image, softened_mask)

        # Perform inpainting to refine the result and make it look natural
        result = pipe(
            prompt=prompt,
            image=guided_image,
            mask_image=softened_mask,  # Use softened mask for inpainting
            strength=0.75,  # Control how much inpainting modifies the image (0.0 to 1.0)
            guidance_scale=7.5  # Control how closely the prompt is followed
        ).images[0]

        # Convert result to bytes for response
        result_bytes = io.BytesIO()
        result.save(result_bytes, format="PNG")
        result_bytes.seek(0)

        # Return the image as a streaming response
        return StreamingResponse(
            result_bytes,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=natural_inpaint_image.png"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during natural inpainting: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)