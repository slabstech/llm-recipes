import cv2
from djitellopy import Tello

def take_picture():

    tello = Tello()
    tello.connect()

    tello.streamon()
    frame_read = tello.get_frame_read()

    tello.takeoff()
    cv2.imwrite("picture.png", frame_read.frame)

    tello.streamoff()
    tello.land()


def main():
    take_picture()

if __name__ == "__main__":
    main()