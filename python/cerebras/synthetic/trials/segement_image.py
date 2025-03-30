import torch
from PIL import Image, ImageDraw, ImageFont
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection 

# Set up model and device
model_id = "IDEA-Research/grounding-dino-base"
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load processor and model
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id).to(device)

# Load local image
image_path = "original.jpg"  # Replace with your local image path
try:
    image = Image.open(image_path).convert("RGB")
except FileNotFoundError:
    print(f"Error: Image file '{image_path}' not found. Please check the path.")
    exit(1)

# Define text query (lowercase with dots as required)
text = "a military tank."  # Modify based on objects in your image

# Prepare inputs for the model
inputs = processor(images=image, text=text, return_tensors="pt").to(device)

# Perform inference
with torch.no_grad():
    outputs = model(**inputs)

# Post-process results
results = processor.post_process_grounded_object_detection(
    outputs,
    inputs.input_ids,
    threshold=0.4,  # Updated parameter
    text_threshold=0.3,
    target_sizes=[image.size[::-1]]  # [width, height]
)

# Debugging: Print results to inspect structure
print("Results:", results)

# Create a copy of the image to draw on
output_image = image.copy()
draw = ImageDraw.Draw(output_image)

# Try to load a font, fall back to default if not available
try:
    font = ImageFont.truetype("arial.ttf", 20)
except:
    font = ImageFont.load_default()

# Colors for different objects
colors = {"a cat": "red", "a remote control": "blue"}  # Adjust based on your text query

# Draw bounding boxes and labels
for detection in results:  # Iterate over the list of detections
    boxes = detection["boxes"]  # Tensor of [x_min, y_min, x_max, y_max]
    labels = detection["labels"]
    scores = detection["scores"]

    for box, label, score in zip(boxes, labels, scores):
        # Convert tensor to list and unpack coordinates
        x_min, y_min, x_max, y_max = box.tolist()
        
        # Draw rectangle
        draw.rectangle(
            [(x_min, y_min), (x_max, y_max)],
            outline=colors.get(label, "green"),  # Default to green if label not in colors
            width=2
        )
        
        # Draw label with score
        label_text = f"{label} {score:.2f}"
        bbox = draw.textbbox((x_min, y_min - 20), label_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Draw background rectangle for text
        draw.rectangle(
            [(x_min, y_min - text_height - 5), (x_min + text_width, y_min)],
            fill=colors.get(label, "green")
        )
        
        # Draw text
        draw.text(
            (x_min, y_min - text_height - 5),
            label_text,
            fill="white",
            font=font
        )

# Save the output image
output_image.save("detected_objects.png", "PNG")
print("Output image saved as 'detected_objects.png'")