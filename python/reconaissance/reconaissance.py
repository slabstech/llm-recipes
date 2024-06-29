from drone_control.record_video import start_360_capture
from drone_control.take_picture import image_capture
from drone_control.vision_query import explain_image
from battlefield.build_map import show_map
from drone_control.model_setup import load_model
import json
import datetime
import os
import requests

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
    image_metadata = '{"time": "2024-06-29 19:14:36", "drone_picture": "drone_control/picture.png", "image_metadata": "\nThe image shows a group of people standing in an airport terminal. There are at least six individuals visible, with some closer to the foreground and others further back. They appear to be waiting or preparing for their flights, as they stand near chairs and dining tables that can be seen throughout the scene. The chairs and tables suggest that this is likely a waiting area within the terminal."}'
    prompt = f"Please analyze the following image metadata and provide additional insights: {json.dumps(image_metadata)}"

    #print(text)
    ollama_endpoint_env = os.environ.get('OLLAMA_ENDPOINT')

    model = "mistral:7b"
    #prompt = text 
    if ollama_endpoint_env is None:
        ollama_endpoint_env = 'http://localhost:11434'
    ollama_endpoint = ollama_endpoint_env +  "/api/generate"  # replace with localhost

    response = requests.post(ollama_endpoint,
                      json={
                          'model': model,
                          'prompt': prompt,
                          'stream':False,
                          'raw': False
                      }, stream=False
                      )
    
    response.raise_for_status()
    result = response.json()

    print(result)

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

if __name__ == "__main__":
    main()