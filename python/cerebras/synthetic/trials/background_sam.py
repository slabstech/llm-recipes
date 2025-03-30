import cv2
import numpy as np
import torch
from transformers import Sam2Processor, Sam2Model

# Load the image
image_path = "original.jpg"  # Replace with your image path
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

# Load the SAM 2 model and processor from Hugging Face
model_name = "facebook/sam2-hiera-tiny"  # You can use "tiny", "small", "base-plus", or "large"
processor = Sam2Processor.from_pretrained(model_name)
model = Sam2Model.from_pretrained(model_name)

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define prompts for background segmentation
# Example: Points on background areas (e.g., sky, ground)
# Format: List of dicts with 'point_coords' (x, y) and 'point_labels' (0 for background, 1 for foreground)
input_points = [
    {"point_coords": [100, 100], "point_labels": 0},  # Background point 1
    {"point_coords": [200, 500], "point_labels": 0},  # Background point 2
]

# Prepare inputs using the processor
inputs = processor(
    images=[image],  # List of images (single image in this case)
    input_points=[input_points],  # List of prompts for each image
    return_tensors="pt"  # Return PyTorch tensors
).to(device)

# Run inference
with torch.no_grad():
    outputs = model(**inputs)

# Get the predicted mask
masks = outputs.pred_masks[0].cpu().numpy()  # Shape: (1, H, W), binary mask
mask = masks[0]  # Take the first mask

# Post-process the mask
# Since we prompted the background, the mask represents the background
background_mask = (mask > 0).astype(np.uint8) * 255  # Convert to 0-255 range

# Apply the mask to the original image
# Option 1: Extract background only
background_image = image.copy()
background_image[background_mask == 0] = 0  # Set foreground to black

# Option 2: Blur the background
blurred_image = cv2.GaussianBlur(image, (21, 21), 0)
foreground_image = image.copy()
foreground_image[background_mask == 255] = blurred_image[background_mask == 255]

# Save or display results
cv2.imwrite("background_only.jpg", cv2.cvtColor(background_image, cv2.COLOR_RGB2BGR))
cv2.imwrite("blurred_background.jpg", cv2.cvtColor(foreground_image, cv2.COLOR_RGB2BGR))

# Optional: Visualize the mask and results
cv2.imshow("Background Mask", background_mask)
cv2.imshow("Background Only", cv2.cvtColor(background_image, cv2.COLOR_RGB2BGR))
cv2.imshow("Blurred Background", cv2.cvtColor(foreground_image, cv2.COLOR_RGB2BGR))
cv2.waitKey(0)
cv2.destroyAllWindows()