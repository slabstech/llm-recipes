#from drone_control.record_video import start_360_capture
from drone_control.take_picture import image_capture
from drone_control.vision_query import explain_image
from drone_control.model_setup import load_model
import json
import os
import requests
import time

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
    

def generate_insights(metadata_file_name):
    # Load data from JSON file
    with open(metadata_file_name, 'r') as f:
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
    metadata_file_name = metadata_file_name.replace('.json', '')

    insight_file_name = f'{metadata_file_name}_insight.json' 
    # Open the file in append mode ('a')
    with open(insight_file_name, 'a') as file:
    # Write the response data to the file
        file.write(str(response_data))
    return insight_file_name
    
def loop_images(directory):
    model = "moondream"
    prompt = "What is in this image?"
    url = "http://localhost:11434"

    # Initialize an empty list to store the metadata
    metadata_list = []
    # get a list of all files in the directory
    files = os.listdir(directory)

    current_epoch = int(time.time())
    # filter the list to only include image files (you can add more extensions if needed)
    image_files = [f for f in files if f.endswith('.jpg') or f.endswith('.png')]

    # process each image
    for image_file in image_files:
        drone_picture = os.path.join(directory, image_file)
        image_metadata = explain_image(drone_picture, model, prompt, url)
            # Add the metadata to the list, including a timestamp
        metadata_list.append({
            'filename': drone_picture,
            'timestamp': time.time(),
            'metadata': image_metadata
        })

    metadata_file_name = f'{current_epoch}_image_metadata.json' 
        # After the loop, write the list to a JSON file
    with open(metadata_file_name, 'w') as f:
        json.dump(metadata_list, f)
        
    return metadata_file_name

def main():
    #drone_video = get_drone_video()
    #drone_picture = get_drone_picture()    
    """
    ollama_url = "http://localhost:11434"
    model_name = "mistral"
    load_model( ollama_url, model_name )

    drone_picture = "drone_control/picture.png"
    """
    #directory = "/home/gaganyatri/code/hackathon/defense_hack/dataset/image_set_1"
    #metada_file_name=  loop_images(directory)
    
    metadata_file_name = "1719715998_image_metadata.json"
    
    insight_file_name = generate_insights(metadata_file_name)

if __name__ == "__main__":
    main()