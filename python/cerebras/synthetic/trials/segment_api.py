from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import torch
from PIL import Image, ImageDraw, ImageFont
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection 
import io

# Initialize FastAPI app
app = FastAPI()

# Set up model and device
model_id = "IDEA-Research/grounding-dino-base"
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load processor and model at startup
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id).to(device)

# Default text query (can be overridden via endpoint parameters)
DEFAULT_TEXT_QUERY = "a tank."  # Adjust based on your use case

def process_image(image: Image.Image, text_query: str = DEFAULT_TEXT_QUERY):
    """Process the image with Grounding DINO and return detection results."""
    # Prepare inputs for the model
    inputs = processor(images=image, text=text_query, return_tensors="pt").to(device)

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Post-process results
    results = processor.post_process_grounded_object_detection(
        outputs,
        inputs.input_ids,
        threshold=0.4,
        text_threshold=0.3,
        target_sizes=[image.size[::-1]]  # [width, height]
    )
    return results

def draw_detections(image: Image.Image, results: list) -> Image.Image:
    """Draw bounding boxes and labels on the image."""
    output_image = image.copy()
    draw = ImageDraw.Draw(output_image)

    # Try to load a font, fall back to default
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    # Colors for different objects
    colors = {"a tank": "red"}  # Add more as needed, e.g., {"a cat": "red", "a remote control": "blue"}

    # Draw bounding boxes and labels
    for detection in results:
        boxes = detection["boxes"]
        labels = detection["labels"]
        scores = detection["scores"]

        for box, label, score in zip(boxes, labels, scores):
            x_min, y_min, x_max, y_max = box.tolist()
            
            # Draw rectangle
            draw.rectangle(
                [(x_min, y_min), (x_max, y_max)],
                outline=colors.get(label, "green"),
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
    
    return output_image

@app.post("/detect-image/")
async def detect_image(
    file: UploadFile = File(..., description="Image file to process"),
    text_query: str = DEFAULT_TEXT_QUERY
):
    """
    Endpoint to detect objects in an image and return the annotated image.
    
    Args:
        file: Uploaded image file.
        text_query: Text query for objects to detect (e.g., "a tank.").
    
    Returns:
        StreamingResponse with the annotated image.
    """
    try:
        # Read and convert the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Process the image
        results = process_image(image, text_query)

        # Draw detections on the image
        output_image = draw_detections(image, results)

        # Convert to bytes for response
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        return StreamingResponse(
            img_byte_arr,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=detected_objects.png"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/detect-json/")
async def detect_json(
    file: UploadFile = File(..., description="Image file to process"),
    text_query: str = DEFAULT_TEXT_QUERY
):
    """
    Endpoint to detect objects in an image and return bounding box information as JSON.
    
    Args:
        file: Uploaded image file.
        text_query: Text query for objects to detect (e.g., "a tank.").
    
    Returns:
        JSONResponse with bounding box coordinates, labels, and scores.
    """
    try:
        # Read and convert the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Process the image
        results = process_image(image, text_query)

        # Format results as JSON-compatible data
        detections = []
        for detection in results:
            boxes = detection["boxes"]
            labels = detection["labels"]
            scores = detection["scores"]

            for box, label, score in zip(boxes, labels, scores):
                x_min, y_min, x_max, y_max = box.tolist()
                detections.append({
                    "label": label,
                    "score": float(score),  # Convert tensor to float
                    "box": {
                        "x_min": x_min,
                        "y_min": y_min,
                        "x_max": x_max,
                        "y_max": y_max
                    }
                })

        return JSONResponse(content={"detections": detections})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)