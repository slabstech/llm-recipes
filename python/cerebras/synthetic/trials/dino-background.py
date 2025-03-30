from transformers import GroundingDinoProcessor, GroundingDinoModel
from segment_anything import SamPredictor, sam_model_registry
import torch
from PIL import Image
import numpy as np
import cv2

# Load Grounding DINO model and processor
def load_grounding_dino(model_name="IDEA-Research/grounding-dino-large"):
    processor = GroundingDinoProcessor.from_pretrained(model_name)
    model = GroundingDinoModel.from_pretrained(model_name)
    return processor, model

# Load SAM model
def load_sam(sam_checkpoint="sam_vit_h_4b8939.pth"):
    sam = sam_model_registry["vit_h"](checkpoint=sam_checkpoint)
    predictor = SamPredictor(sam)
    return predictor

# Perform object detection with Grounding DINO
def detect_objects(processor, model, image_path, text_prompt):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, text=text_prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    # Extract bounding boxes and scores
    boxes = outputs.pred_boxes[0].cpu().numpy()  # Bounding boxes
    scores = outputs.pred_scores[0].cpu().numpy()  # Confidence scores
    return image, boxes, scores

# Segment objects using SAM
def segment_with_sam(predictor, image_pil, boxes):
    image_np = np.array(image_pil)
    predictor.set_image(image_np)
    transformed_boxes = predictor.transform.apply_boxes_torch(
        torch.tensor(boxes), image_np.shape[:2]
    )
    masks, _, _ = predictor.predict_torch(
        point_coords=None,
        point_labels=None,
        boxes=transformed_boxes,
        multimask_output=True,
    )
    return masks[0].cpu().numpy()

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
