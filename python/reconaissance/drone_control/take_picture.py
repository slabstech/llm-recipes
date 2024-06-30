import cv2
from djitellopy import Tello

def image_capture(file_name_for_image):

    tello = Tello()
    tello.connect()

    tello.streamon()
    frame_read = tello.get_frame_read()

    tello.takeoff()
    cv2.imwrite(file_name_for_image, frame_read.frame)

    tello.streamoff()
    tello.land()


def main():
    file_name_for_image = "picture.png"
    image_capture(file_name_for_image)

if __name__ == "__main__":
    main()