import cv2
from djitellopy import Tello
import time
def image_capture(file_name_for_image):

    tello = Tello()
    tello.connect()

    tello.streamon()
    frame_read = tello.get_frame_read()

    tello.takeoff()
    counter = 0
    tello.rotate_counter_clockwise(360)
    while True:
        # Capture frame-by-frame

        # Save the frame as an image every second
        if time.time() % 1 < 0.01:
            file_name_for_image = f'image22_{counter}.jpg'
            cv2.imwrite(file_name_for_image, frame_read.frame)
            counter += 1
        if counter > 10:
            break


    tello.streamoff()
    tello.land()


def main():
    file_name_for_image = "picture.png"
    image_capture(file_name_for_image)

if __name__ == "__main__":
    main()