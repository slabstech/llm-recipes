import cv2
from djitellopy import Tello
import time
def image_capture(file_name_for_image):

    tello = Tello()
    tello.connect()

    tello.streamon()
    frame_read = tello.get_frame_read()

    tello.takeoff()
    tello.move_up(75)
    max_time = 10
    counter = 0
    #tello.rotate_clockwise(360)
    current_epoch = int(time.time())
    while True:
        # Capture frame-by-frame
        file_name_for_image = f'image_{current_epoch}_b_{counter}.jpg'
        cv2.imwrite(file_name_for_image, frame_read.frame)
        counter += 1
        if counter > max_time:
            break
        time.sleep(1)  # Add a 1 second sleep

    tello.streamoff()
    tello.land()


def main():
    file_name_for_image = "picture.png"
    image_capture(file_name_for_image)

if __name__ == "__main__":
    main()