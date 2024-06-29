import requests
import base64

def hover_drone():
    print("hover drone")

def start_360_capture():
    print("started capture")

def send_video():
    print("send video")

def hover_up(): 
    print("Going up")

def hover_down():
    print("Going down")

def main():
    hover_drone()
    hover_up()
    start_360_capture()
    hover_down()
    send_video()

if __name__ == "__main__":
    main()

