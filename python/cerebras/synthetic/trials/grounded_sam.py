from autodistill_grounded_sam_2 import GroundedSAM2
from autodistill.detection import CaptionOntology
from autodistill.utils import plot
import cv2
import supervision as sv

base_model = GroundedSAM2(
	ontology=CaptionOntology(
    	{
        	"screw": "screw"
    	}
	)
)
results = base_model.predict("original.jpg")

image = cv2.imread("original.jpg")

mask_annotator = sv.MaskAnnotator()

annotated_image = mask_annotator.annotate(
	image.copy(), detections=results
)

sv.plot_image(image=annotated_image, size=(8, 8))