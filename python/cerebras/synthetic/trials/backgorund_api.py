from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import torch
from PIL import Image
import io
import numpy as np
import cv2
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
from sam2.sam2_image_predictor import SAM2ImagePredictor

# Initialize FastAPI app
app = FastAPI()

# Set up device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Grounding DINO model and processor at startup
dino_model_id = "IDEA-Research/grounding-dino-base"
dino_processor = AutoProcessor.from_pretrained(dino_model_id)
dino_model = AutoModelForZeroShotObjectDetection.from_pretrained(dino_model_id).to(device)

# Load SAM 2 model at startup
#sam_checkpoint = "sam2.1_hiera_tiny.pt"  # Replace with your checkpoint path
sam_predictor = SAM2ImagePredictor.from_pretrained("facebook/sam2-hiera-tiny")
sam_predictor.model.to(device)

# Default text query
DEFAULT_TEXT_QUERY = "a tank."

def process_image_with_dino(image: Image.Image, text_query: str = DEFAULT_TEXT_QUERY):
    """Detect objects using Grounding DINO."""
    inputs = dino_processor(images=image, text=text_query, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = dino_model(**inputs)

    # Post-process results
    results = dino_processor.post_process_grounded_object_detection(
        outputs,
        inputs.input_ids,
        threshold=0.4,
        text_threshold=0.3,
        target_sizes=[image.size[::-1]]  # [width, height]
    )
    return results[0]  # Single image result

def segment_with_sam(image: Image.Image, boxes: list):
    """Segment detected objects using SAM 2 and return a mask."""
    image_np = np.array(image)
    sam_predictor.set_image(image_np)

    if not boxes:
        return np.zeros(image_np.shape[:2], dtype=bool)  # Empty mask if no boxes

    # Convert boxes to [x_min, y_min, x_max, y_max] tensor and move to device
    boxes_tensor = torch.tensor(
        [[box["x_min"], box["y_min"], box["x_max"], box["y_max"]] for box in boxes],
        dtype=torch.float32
    ).to(device)

    # Predict with SAM 2 using boxes directly
    masks, _, _ = sam_predictor.predict(
        point_coords=None,
        point_labels=None,
        box=boxes_tensor,  # Use 'box' argument instead of 'boxes'
        multimask_output=False
    )
    return masks[0]  # Return the first mask directly (already a NumPy array)

def create_background_mask(image_np: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Create an RGB mask for background removal."""
    mask_inv = np.logical_not(mask).astype(np.uint8) * 255  # Invert mask (background is white)
    mask_rgb = cv2.cvtColor(mask_inv, cv2.COLOR_GRAY2RGB)  # Convert to RGB
    return mask_rgb

@app.post("/detect-json/")
async def detect_json(
    file: UploadFile = File(..., description="Image file to process"),
    text_query: str = DEFAULT_TEXT_QUERY
):
    """Endpoint to detect objects and return bounding box information as JSON."""
    try:
        # Read and convert the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Process with Grounding DINO
        results = process_image_with_dino(image, text_query)

        # Format results as JSON-compatible data
        detections = []
        for box, label, score in zip(results["boxes"], results["labels"], results["scores"]):
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

@app.post("/segment-image/")
async def segment_image(
    file: UploadFile = File(..., description="Image file to process"),
    text_query: str = DEFAULT_TEXT_QUERY
):
    """Endpoint to segment objects and return the image with background removed."""
    try:
        # Read and convert the uploaded image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Detect objects with Grounding DINO
        results = process_image_with_dino(image, text_query)

        # Extract boxes for segmentation, move to CPU
        boxes = [
            {"x_min": box[0].item(), "y_min": box[1].item(), "x_max": box[2].item(), "y_max": box[3].item()}
            for box in results["boxes"].cpu()  # Move tensor to CPU here
        ]

        # Segment with SAM 2
        mask = segment_with_sam(image, boxes)

        # Create background mask and apply it
        image_np = np.array(image)
        background_mask = create_background_mask(image_np, mask)
        segmented_image = cv2.bitwise_and(image_np, background_mask)

        # Convert to PIL Image and save to bytes
        output_image = Image.fromarray(segmented_image)
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        return StreamingResponse(
            img_byte_arr,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=segmented_image.png"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)