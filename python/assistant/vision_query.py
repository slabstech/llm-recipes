import requests
import base64
import json 
import time
import os
def explain_image(image_path, model, prompt, ollama_url):
        
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())

    url = ollama_url + "/api/chat"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [encoded_image.decode("utf-8")]
            }
        ]
    }
    
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
                content = data_list['message']['content']
                response_data += content
    else:
        print(f"Error: {response.status_code} - {response.text}")
    return response_data


def explain_images_directory(directory, model, prompt, url):

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
 
    # Load the prompt from a JSON file
    with open('prompt.json', 'r') as f:
        prompt_data = json.load(f)

    model = prompt_data['model']
    prompt = prompt_data['prompt']
    url = prompt_data['url']
        
    image_inference = explain_image("../../docs/images/speech-inference.png", model, prompt, url)    
    print(image_inference)

if __name__ == "__main__":
    main()

