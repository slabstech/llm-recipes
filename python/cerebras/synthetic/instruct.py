from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
import io
import math
from PIL import Image, ImageOps
import torch
from diffusers import StableDiffusionInstructPix2PixPipeline

# Initialize FastAPI app
app = FastAPI()

# Load the pre-trained model once at startup
model_id = "timbrooks/instruct-pix2pix"
pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(
    model_id, torch_dtype=torch.float16, safety_checker=None
).to("cuda")

# Default configuration values
DEFAULT_STEPS = 50
DEFAULT_TEXT_CFG = 7.5
DEFAULT_IMAGE_CFG = 1.5
DEFAULT_SEED = 1371

def process_image(input_image: Image.Image, instruction: str, steps: int, text_cfg_scale: float, image_cfg_scale: float, seed: int):
    """
    Process the input image with the given instruction using InstructPix2Pix.
    """
    # Resize image to fit model requirements
    width, height = input_image.size
    factor = 512 / max(width, height)
    factor = math.ceil(min(width, height) * factor / 64) * 64 / min(width, height)
    width = int((width * factor) // 64) * 64
    height = int((height * factor) // 64) * 64
    input_image = ImageOps.fit(input_image, (width, height), method=Image.Resampling.LANCZOS)

    if not instruction:
        return input_image

    # Set the random seed for reproducibility
    generator = torch.manual_seed(seed)

    # Generate the edited image
    edited_image = pipe(
        instruction,
        image=input_image,
        guidance_scale=text_cfg_scale,
        image_guidance_scale=image_cfg_scale,
        num_inference_steps=steps,
        generator=generator,
    ).images[0]

    return edited_image

@app.post("/edit-image/")
async def edit_image(
    file: UploadFile = File(...),
    instruction: str = Form(...),
    steps: int = Form(default=DEFAULT_STEPS),
    text_cfg_scale: float = Form(default=DEFAULT_TEXT_CFG),
    image_cfg_scale: float = Form(default=DEFAULT_IMAGE_CFG),
    seed: int = Form(default=DEFAULT_SEED)
):
    """
    Endpoint to edit an image based on a text instruction.
    - file: The input image to edit.
    - instruction: The text instruction for editing the image.
    - steps: Number of inference steps.
    - text_cfg_scale: Text CFG weight.
    - image_cfg_scale: Image CFG weight.
    - seed: Random seed for reproducibility.
    """
    # Read and convert the uploaded image
    image_data = await file.read()
    input_image = Image.open(io.BytesIO(image_data)).convert("RGB")

    # Process the image
    edited_image = process_image(input_image, instruction, steps, text_cfg_scale, image_cfg_scale, seed)

    # Convert the edited image to bytes
    img_byte_arr = io.BytesIO()
    edited_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    # Return the image as a streaming response
    return StreamingResponse(img_byte_arr, media_type="image/png")

@app.get("/")
async def root():
    """
    Root endpoint for basic health check.
    """
    return {"message": "InstructPix2Pix API is running. Use POST /edit-image/ to edit images."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)