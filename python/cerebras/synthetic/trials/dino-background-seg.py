from transformers import GroundingDinoProcessor, GroundingDinoForObjectDetection
from segment_anything import SamPredictor, sam_model_registry
import torch
from PIL import Image
import numpy as np
import cv2

# Load Grounding DINO model and processor
def load_grounding_dino(model_name="IDEA-Research/grounding-dino-base"):
    processor = GroundingDinoProcessor.from_pretrained(model_name)
    model = GroundingDinoForObjectDetection.from_pretrained(model_name)
    return processor, model

# Load SAM model
def load_sam(sam_checkpoint="sam_vit_h_4b8939.pth"):
    sam = sam_model_registry["vit_h"](checkpoint=sam_checkpoint)
    predictor = SamPredictor(sam)
    return predictor

# Perform object detection with Grounding DINO
def detect_objects(processor, model, image_path, text_prompt, confidence_threshold=0.3):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, text=text_prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    # Extract logits and boxes from outputs
    logits = outputs.logits.sigmoid().cpu().numpy()[0]  # [num_queries]
    boxes = outputs.pred_boxes.cpu().numpy()[0]         # [num_queries, 4] in [x_center, y_center, w, h]

    # Filter detections based on confidence threshold
    scores = logits  # Confidence scores
    valid_indices = scores > confidence_threshold
    filtered_boxes = boxes[valid_indices, :]  # Filter boxes (correct indexing)
    filtered_scores = scores[valid_indices]   # Filter scores

    # Scale boxes to image dimensions (assuming boxes are normalized between 0-1)
    if len(filtered_boxes) > 0:  # Only scale if there are valid detections
        img_width, img_height = image.size
        filtered_boxes[:, [0, 2]] *= img_width   # Scale x_center and width
        filtered_boxes[:, [1, 3]] *= img_height  # Scale y_center and height
    else:
        print("No objects detected above confidence threshold.")

    return image, filtered_boxes, filtered_scores

# Segment objects using SAM
def segment_with_sam(predictor, image_pil, boxes):
    image_np = np.array(image_pil)
    predictor.set_image(image_np)
    if len(boxes) == 0:  # Handle case with no detections
        return np.zeros(image_np.shape[:2], dtype=bool)  # Return empty mask
    
    # Convert boxes from [x_center, y_center, w, h] to [x1, y1, x2, y2] for SAM
    boxes_xyxy = np.zeros_like(boxes)
    boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2  # x1 = x_center - w/2
    boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2  # y1 = y_center - h/2
    boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2  # x2 = x_center + w/2
    boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2  # y2 = y_center + h/2

    transformed_boxes = predictor.transform.apply_boxes_torch(
        torch.tensor(boxes_xyxy), image_np.shape[:2]
    )
    masks, _, _ = predictor.predict_torch(
        point_coords=None,
        point_labels=None,
        boxes=transformed_boxes,
        multimask_output=True,
    )
    return masks[0].cpu().numpy()  # Take the first mask

# Create a mask for background removal
def create_background_mask(image_np, mask):
    mask_inv = np.logical_not(mask).astype(np.uint8) * 255  # Invert mask (background is white)
    mask_rgb = cv2.cvtColor(mask_inv, cv2.COLOR_GRAY2RGB)  # Convert to RGB format
    return mask_rgb

# Main function to run the pipeline
def main():
    # Paths to models and input image
    grounding_dino_model_name = "IDEA-Research/grounding-dino-base"
    sam_checkpoint_path = "sam_vit_h_4b8939.pth"
    input_image_path = "original.jpg"  # Replace with your input image path
    text_prompt = "tank"  # Replace with your desired object prompt
    
    # Load models
    processor, grounding_dino_model = load_grounding_dino(grounding_dino_model_name)
    sam_predictor = load_sam(sam_checkpoint_path)

    # Detect objects with Grounding DINO
    image_pil, boxes, scores = detect_objects(processor, grounding_dino_model, input_image_path, text_prompt)

    # Segment objects with SAM
    mask = segment_with_sam(sam_predictor, image_pil, boxes)

    # Create a background mask and apply it to the original image
    image_np = np.array(image_pil)
    background_mask = create_background_mask(image_np, mask)

    # Save the output mask and segmented image
    cv2.imwrite("background_mask.png", background_mask)
    
    # Apply the mask to remove the background from the original image
    segmented_image = cv2.bitwise_and(image_np, background_mask)
    
    segmented_output_path = "segmented_output.png"
    cv2.imwrite(segmented_output_path, segmented_image)

    print(f"Background segmentation completed! Output saved as {segmented_output_path}")

if __name__ == "__main__":
    main()