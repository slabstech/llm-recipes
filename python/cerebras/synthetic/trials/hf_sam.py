import torch
from sam2.sam2_image_predictor import SAM2ImagePredictor
from PIL import Image
import numpy as np
predictor = SAM2ImagePredictor.from_pretrained("facebook/sam2.1-hiera-tiny")



image = Image.open('images/truck.jpg')
image = np.array(image.convert("RGB"))


with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
    predictor.set_image("original.jpg")
    masks, _, _ = predictor.predict("find")