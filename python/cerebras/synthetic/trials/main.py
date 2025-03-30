from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess
import os
import shutil
import tempfile
import zipfile
from diffusers import StableDiffusionInstructPix2PixPipeline
import torch
from PIL import Image
import json
app = FastAPI()

# Load InstructPix2Pix model
pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(
    "timm/instruct-pix2pix",
    torch_dtype=torch.float16,
    safety_checker=None,
).to("cuda")

class DatasetRequest(BaseModel):
    objects: list[str]
    environment: str
    num_images: int
    augmentation_prompts: list[str]

def augment_image(image_path, prompt):
    image = Image.open(image_path).convert("RGB")
    augmented = pipe(prompt=prompt, image=image, num_inference_steps=20, image_guidance_scale=1.5).images[0]
    return augmented

@app.post("/generate_dataset")
async def generate_dataset(request: DatasetRequest):
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Step 1: Generate base images with Blender
            base_dir = os.path.join(tmpdirname, "base")
            os.makedirs(base_dir)
            subprocess.run([
                "blender", "--background", "--python", "blender_script.py", "--",
                ",".join(request.objects), request.environment, str(request.num_images), base_dir
            ], check=True)
            
            # Load base annotations
            with open(os.path.join(base_dir, "annotations.json"), "r") as f:
                base_annotations = json.load(f)
            
            # Step 2: Augment images
            output_dir = os.path.join(tmpdirname, "output/images")
            os.makedirs(output_dir)
            annotations = []
            image_id = 0
            for base_anno in base_annotations:
                base_image_path = os.path.join(base_dir, base_anno["file_name"])
                for prompt in request.augmentation_prompts:
                    augmented = augment_image(base_image_path, prompt)
                    new_filename = f"image_{image_id}.png"
                    augmented.save(os.path.join(output_dir, new_filename))
                    annotations.append({
                        "image_id": image_id,
                        "file_name": new_filename,
                        "labels": base_anno["labels"]
                    })
                    image_id += 1
            
            # Save annotations
            anno_file = os.path.join(tmpdirname, "output/annotations.json")
            with open(anno_file, "w") as f:
                json.dump(annotations, f)
            
            # Step 3: Create zip file
            zip_path = os.path.join(tmpdirname, "dataset.zip")
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for root, _, files in os.walk(output_dir):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.join("images", file))
                zipf.write(anno_file, "annotations.json")
            
            return FileResponse(zip_path, media_type="application/zip", filename="dataset.zip")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)