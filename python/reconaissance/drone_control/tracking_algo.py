import os
import supervision as sv
import numpy as np
from ultralytics import YOLO
import logging

import cv2
import time
import torch
 
logging.getLogger('ultralytics').setLevel(logging.WARNING)
logging.getLogger('supervision').setLevel(logging.WARNING)

#ROOT_PATH = "/home/gaganyatri/Downloads"
#VIDEO_PATH = os.path.join(ROOT_PATH, "IMG_9537.MOV")


import time, cv2
from threading import Thread
from djitellopy import Tello

from record_video import start_360_capture

def load_model():
    model = YOLO("yolov10l.pt", verbose=False)
    return model


def process_frame(model, frame: np.ndarray, _) -> np.ndarray:
    results = model(frame, imgsz=frame.shape[:2])[0]
    results_dict = results.boxes.data
    results_dict.pred = [results_dict]
    boxes = results.boxes.cpu().numpy()
    detections = results.boxes.data.cpu().cpu().numpy() #sv.Detections.from_yolov5(results.boxes.data) #from_yolov8(results)
    dets = sv.Detections.from_yolov5(results_dict)
    box_annotator = sv.BoxAnnotator(thickness=4, text_thickness=4, text_scale=2)
    # box_annotator = sv.BoundingBoxAnnotator(thickness=4, text_thickness=4, text_scale=2)

    # labels = [f"{model.names[class_id]} {confidence:0.2f}" for _, _, confidence, class_id, _ in detections]

    labels = [f"{model.names[class_id]} {confidence:0.2f}" for _, _, _, _, confidence, class_id in detections]
    frame = box_annotator.annotate(scene=frame, detections=dets, labels=labels)

    return frame, results.boxes.xywh



def select_object_to_track(detected_objects):
    if len(detected_objects):
        return detected_objects[0]
    return None

def track_object(video_info, bbox):
    frame_center_x = video_info.width // 2
    frame_center_y = video_info.height // 2

    # x, y, w, h = bbox
    x, y, w, h = map(int, bbox)
    object_center_x = x + w // 2
    object_center_y = y + h // 2

    error_x = object_center_x - frame_center_x
    error_y = object_center_y - frame_center_y

    # # Draw error lines
    # cv2.line(frame, (frame_center_x, frame_center_y), (object_center_x, frame_center_y), (0, 0, 255), 2)
    # cv2.line(frame, (object_center_x, frame_center_y), (object_center_x, object_center_y), (0, 255, 0), 2)
    # # sv.draw_text(frame, f"error_x: {error_x}", (10, 30), scale=1, color=(0, 0, 255), thickness=2)
    # # sv.draw_text(frame, f"error_y: {error_y}", (10, 60), scale=1, color=(0, 255, 0), thickness=2)

    # # Draw text using OpenCV
    # cv2.putText(frame, f"error_x: {error_x}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # cv2.putText(frame, f"error_y: {error_y}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    threshold = 20
    k = 0.1

    if abs(error_x) > threshold:
        if error_x > 0:
            print("Move right: ", k * abs(error_x))
            # tello.move_right(int(k * abs(error_x)))
        else:
            print("Move left: ", k * abs(error_x))
            # tello.move_left(int(k * abs(error_x)))

    if abs(error_y) > threshold:
        if error_y > 0:
            print("Move down: ", k * abs(error_y))
            # tello.move_down(int(k * abs(error_y)))
        else:
            print("Move up: ", k * abs(error_y))
            # tello.move_up(int(k * abs(error_y)))

# while True:



def main():
    print("run tracking")
    model =load_model()
    file_name_for_video = "drone_360_video.avi"
    start_360_capture(file_name_for_video)
    video_info = sv.VideoInfo.from_video_path(file_name_for_video)

    for index, frame in enumerate(
        sv.get_video_frames_generator(source_path=source_path)
        ):
        if index > 50:
            break
        frame, detected_objects = process_frame(model,frame,index)
        object_to_track = select_object_to_track(detected_objects)
        
        if type(object_to_track) is torch.Tensor:
            if len(object_to_track):
                track_object(video_info,object_to_track)
    

if __name__ == "__main__":
    main()