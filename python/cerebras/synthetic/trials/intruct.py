from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
import io
import math
from PIL import Image, ImageOps, ImageDraw
import torch
from diffusers import StableDiffusionInstructPix2PixPipeline, StableDiffusionInpaintPipeline
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
import torch
from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler
from huggingface_hub import hf_hub_download, login
from safetensors.torch import load_file
from io import BytesIO
import os
import base64
from typing import List

# Initialize FastAPI app
app = FastAPI()

# Load the pre-trained InstructPix2Pix model for editing
model_id = "timbrooks/instruct-pix2pix"
pipe_edit = StableDiffusionInstructPix2PixPipeline.from_pretrained(
    model_id, torch_dtype=torch.float16, safety_checker=None
).to("cuda")

# Load the pre-trained Inpainting model
inpaint_model_id = "stabilityai/stable-diffusion-2-inpainting"
pipe_inpaint = StableDiffusionInpaintPipeline.from_pretrained(
    inpaint_model_id, torch_dtype=torch.float16, safety_checker=None
).to("cuda")

# Default configuration values
DEFAULT_STEPS = 50
DEFAULT_TEXT_CFG = 7.5
DEFAULT_IMAGE_CFG = 1.5
DEFAULT_SEED = 1371

HF_TOKEN = os.getenv("HF_TOKEN")

def load_model():
    try:
        # Login to Hugging Face if token is provided
        if HF_TOKEN:
            login(token=HF_TOKEN)
            
        base = "stabilityai/stable-diffusion-xl-base-1.0"
        repo = "ByteDance/SDXL-Lightning"
        ckpt = "sdxl_lightning_4step_unet.safetensors"

        # Load model with explicit error handling
        unet = UNet2DConditionModel.from_config(
            base, 
            subfolder="unet"
        ).to("cuda", torch.float16)
        
        unet.load_state_dict(load_file(hf_hub_download(repo, ckpt), device="cuda"))
        pipe = StableDiffusionXLPipeline.from_pretrained(
            base, 
            unet=unet, 
            torch_dtype=torch.float16, 
            variant="fp16"
        ).to("cuda")
        
        # Configure scheduler
        pipe.scheduler = EulerDiscreteScheduler.from_config(
            pipe.scheduler.config, 
            timestep_spacing="trailing"
        )
        
        return pipe
    
    except Exception as e:
        raise Exception(f"Failed to load model: {str(e)}")

# Load model at startup with error handling
try:
    pipe_generate = load_model()
except Exception as e:
    print(f"Model initialization failed: {str(e)}")
    raise

@app.get("/generate")
async def generate_image(prompt: str):
    try:
        # Generate image
        image = pipe_generate(
            prompt,
            num_inference_steps=4,
            guidance_scale=0
        ).images[0]
        
        # Save image to buffer
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        
        return Response(content=buffer.getvalue(), media_type="image/png")
    
    except Exception as e:
        return {"error": str(e)}

@app.get("/generate_multiple")
async def generate_multiple_images(prompts: List[str]):
    try:
        # List to store base64-encoded images
        generated_images = []
        
        # Generate an image for each prompt
        for prompt in prompts:
            image = pipe_generate(
                prompt,
                num_inference_steps=4,
                guidance_scale=0
            ).images[0]
            
            # Save image to buffer
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
            
            # Encode the image as base64
            image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            generated_images.append({
                "prompt": prompt,
                "image_base64": image_base64
            })
        
        return {"images": generated_images}
    
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

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
    edited_image = pipe_edit(
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

# New endpoint for inpainting
@app.post("/inpaint/")
async def inpaint_image(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    mask_coordinates: str = Form(...),  # Format: "x1,y1,x2,y2" (top-left and bottom-right of the rectangle to inpaint)
    steps: int = Form(default=DEFAULT_STEPS),
    guidance_scale: float = Form(default=7.5),
    seed: int = Form(default=DEFAULT_SEED)
):
    """
    Endpoint to perform inpainting on an image.
    - file: The input image to inpaint.
    - prompt: The text prompt describing what to generate in the inpainted area.
    - mask_coordinates: Coordinates of the rectangular area to inpaint (format: "x1,y1,x2,y2").
    - steps: Number of inference steps.
    - guidance_scale: Guidance scale for the inpainting process.
    - seed: Random seed for reproducibility.
    """
    try:
        # Read and convert the uploaded image
        image_data = await file.read()
        input_image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Resize image to fit model requirements (must be divisible by 8 for inpainting)
        width, height = input_image.size
        factor = 512 / max(width, height)
        factor = math.ceil(min(width, height) * factor / 8) * 8 / min(width, height)
        width = int((width * factor) // 8) * 8
        height = int((height * factor) // 8) * 8
        input_image = ImageOps.fit(input_image, (width, height), method=Image.Resampling.LANCZOS)

        # Create a mask for inpainting
        mask = Image.new("L", (width, height), 0)  # Black image (0 = no inpainting)
        draw = ImageDraw.Draw(mask)

        # Parse the mask coordinates
        try:
            x1, y1, x2, y2 = map(int, mask_coordinates.split(","))
            # Adjust coordinates based on resized image
            x1 = int(x1 * factor)
            y1 = int(y1 * factor)
            x2 = int(x2 * factor)
            y2 = int(y2 * factor)
        except ValueError:
            return {"error": "Invalid mask coordinates format. Use 'x1,y1,x2,y2'."}

        # Draw a white rectangle on the mask (255 = area to inpaint)
        draw.rectangle([x1, y1, x2, y2], fill=255)

        # Set the random seed for reproducibility
        generator = torch.manual_seed(seed)

        # Perform inpainting
        inpainted_image = pipe_inpaint(
            prompt=prompt,
            image=input_image,
            mask_image=mask,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            generator=generator,
        ).images[0]

        # Convert the inpainted image to bytes
        img_byte_arr = io.BytesIO()
        inpainted_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        # Return the image as a streaming response
        return StreamingResponse(img_byte_arr, media_type="image/png")

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    """
    Root endpoint for basic health check.
    """
    return {"message": "InstructPix2Pix API is running. Use POST /edit-image/ or /inpaint/ to edit images."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)