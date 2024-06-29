from drone_control.record_video import start_360_capture
from drone_control.take_picture import image_capture

def get_drone_video():
    print("getting drone video")
    file_name_for_video = "drone_360_video.avi"
    start_360_capture(file_name_for_video)
    return file_name_for_video

def get_drone_picture():
    print("getting dorne picture")
    file_name_for_image = "picture.png"
    image_capture(file_name_for_image)
    return file_name_for_image
    
def main():
    #drone_video = get_drone_video()
    drone_pitcure = get_drone_picture()



if __name__ == "__main__":
    main()