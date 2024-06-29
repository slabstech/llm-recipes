from drone_control.record_video import start_360_capture
from drone_control.take_picture import image_capture
from drone_control.vision_query import explain_image
from battlefield.build_map import show_map
from drone_control.model_setup import load_model
import json
import datetime
import os
import requests
from PIL import Image


def get_image_exif():
    # Open the image file
    with Image.open('drone_control/picture.png') as img:
        # Get the image metadata
        metadata = img.info

    # Print the metadata
    print(metadata)


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
    
def store_image_metadata(image_metadata, drone_picture):
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

def process_metadata():
    generate_insights("ss")


def generate_insights(image_metadata):
    # Mistral API endpoint
#    image_metadata = '{"time": "2024-06-29 19:14:36", "drone_picture": "drone_control/picture.png", "image_metadata": "\nThe image shows a group of people standing in an airport terminal. There are at least six individuals visible, with some closer to the foreground and others further back. They appear to be waiting or preparing for their flights, as they stand near chairs and dining tables that can be seen throughout the scene. The chairs and tables suggest that this is likely a waiting area within the terminal."}'
    # Load data from JSON file
    with open('data.json', 'r') as f:
        data = json.load(f)

    prompt = f"Please analyze the following json data : {data}, return short info if there is any difference across time"

    ollama_url = "http://localhost:11434"
    model_name = "mistral"

    command = "/api/generate"
    url = ollama_url + command
    model = model_name + ":latest"
    payload = {"model": model, "prompt":prompt}
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)

    response_data = ""
    if response.status_code == 200:
        for chunk in response.iter_lines():
            if chunk:
                data = chunk.decode('utf-8')
                data_list = json.loads(data)
                content = data_list['response']
                response_data += content
    else:
        print(f"Error: {response.status_code} - {response.text}")

    print(response_data)
    # Open the file in append mode ('a')
    with open('response_data.txt', 'a') as file:
    # Write the response data to the file
        file.write(str(response_data))
    return response_data
    

def main():
    #drone_video = get_drone_video()
    #drone_picture = get_drone_picture()    
    """
    ollama_url = "http://localhost:11434"
    model_name = "mistral"
    load_model( ollama_url, model_name )

    drone_picture = "drone_control/picture.png"
    """
    """
    model = "moondream"
    prompt = "What is in this image?"
            
    url = "http://localhost:11434"
        
    image_metadata = explain_image(drone_picture, model, prompt, url)    
    
    store_image_metadata(image_metadata, drone_picture)
    """

    process_metadata()
    # get_image_exif()

if __name__ == "__main__":
    main()