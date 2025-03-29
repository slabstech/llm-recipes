from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, Response
from PIL import Image
import io
import torch
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
    return {"message": "InstructPix2Pix API is running. Use POST /edit-image/ or /inpaint/ to edit images."}

@app.post("/inpaint/")
async def inpaint_image(
    image: UploadFile = File(...),
    mask: UploadFile = File(...),
    prompt: str = "Fill the masked area with appropriate content."
):
    """
    Endpoint for image inpainting.
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)