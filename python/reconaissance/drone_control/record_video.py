import time, cv2
from threading import Thread
from djitellopy import Tello

def start_360_capture():
    tello = Tello()

    tello.connect()

    keepRecording = True
    tello.streamon()
    frame_read = tello.get_frame_read()

    recorder = Thread(target=videoRecorder)
    recorder.start()

    tello.takeoff()
    tello.move_up(100)
    tello.rotate_counter_clockwise(360)

    tello.streamoff()
    tello.land()

    keepRecording = False
    recorder.join()

def videoRecorder():

    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()

def main():
    start_360_capture()

if __name__ == "__main__":
    main()
