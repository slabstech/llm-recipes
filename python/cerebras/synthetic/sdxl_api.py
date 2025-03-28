from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
import torch
from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler
from huggingface_hub import hf_hub_download, login
from safetensors.torch import load_file
from io import BytesIO
import os

app = FastAPI()

# Get Hugging Face token from environment variable
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
    pipe = load_model()
except Exception as e:
    print(f"Model initialization failed: {str(e)}")
    raise

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
        
        return Response(content=buffer.getvalue(), media_type="image/png")
    
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)