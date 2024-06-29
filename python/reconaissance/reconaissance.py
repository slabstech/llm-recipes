from drone_control.record_video import start_360_capture
from drone_control.take_picture import image_capture
from drone_control.vision_query import explain_image
from battlefield.build_map import show_map
from drone_control.model_setup import load_model
import json

import datetime

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
    #drone_picture = get_drone_picture()    

    ollama_url = "http://localhost:11434"
    model_name = "moondream"
    #load_model( ollama_url, model_name )

    drone_picture = "drone_control/picture.png"

    model = "moondream"
    prompt = "What is in this image?"
            
    url = "http://localhost:11434"
        
    image_metadata = explain_image(drone_picture, model, prompt, url)    
    #print(image_metadata)
    
    # Get the current time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a dictionary to store the data
    data = {
        "time": current_time,
        "drone_picture": drone_picture,
        "image_metadata": image_metadata
    }

    # Write the data to a JSON file
    with open('data.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')
        #show_map()



if __name__ == "__main__":
    main()