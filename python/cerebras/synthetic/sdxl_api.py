from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
import torch
from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
from io import BytesIO
import os

app = FastAPI()

# Initialize the model once when the server starts
def load_model():
    base = "stabilityai/stable-diffusion-xl-base-1.0"
    repo = "ByteDance/SDXL-Lightning"
    ckpt = "sdxl_lightning_4step_unet.safetensors"

    # Load model
    unet = UNet2DConditionModel.from_config(base, subfolder="unet").to("cuda", torch.float16)
    unet.load_state_dict(load_file(hf_hub_download(repo, ckpt), device="cuda"))
    pipe = StableDiffusionXLPipeline.from_pretrained(base, unet=unet, torch_dtype=torch.float16, variant="fp16").to("cuda")
    
    # Configure scheduler
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")
    
    return pipe

# Load model at startup
pipe = load_model()

@app.get("/generate")
async def generate_image(prompt: str):
    try:
        # Generate image
        image = pipe(
            prompt,
            num_inference_steps=4,
            guidance_scale=0
        ).images[0]
        
        # Save image to buffer
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Return image as response
        return Response(content=buffer.getvalue(), media_type="image/png")
    
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    