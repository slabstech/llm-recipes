import time, cv2
from threading import Thread
from djitellopy import Tello

def start_360_capture(file_name_for_video):
    tello = Tello()

    tello.connect()

    keepRecording = True
    tello.streamon()
    frame_read = tello.get_frame_read()

    recorder = Thread(target=videoRecorder(file_name_for_video))
    recorder.start()

    tello.takeoff()
    tello.move_up(100)
    tello.rotate_counter_clockwise(360)

    tello.streamoff()
    tello.land()

    keepRecording = False
    recorder.join()

def videoRecorderfile_name_for_video

    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter(file_name_for_video, cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()

def main():
    file_name_for_video = "drone_360_video.avi"
    start_360_capture(file_name_for_video)

if __name__ == "__main__":
    main()
