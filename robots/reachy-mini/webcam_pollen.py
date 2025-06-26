import cv2

from pollen_vision.vision_models.object_detection import OwlVitWrapper
from pollen_vision.vision_models.object_segmentation import MobileSamWrapper
from pollen_vision.utils import Annotator, get_bboxes


owl = OwlVitWrapper()
sam = MobileSamWrapper()
annotator = Annotator()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    predictions = owl.infer(
        frame, ["paper cups"]
    )  # zero-shot object detection | put your classes here
    bboxes = get_bboxes(predictions)

    masks = sam.infer(frame, bboxes=bboxes)  # zero-shot object segmentation
    annotated_frame = annotator.annotate(frame, predictions, masks=masks)

    cv2.imshow("frame", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break