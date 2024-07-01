import requests
import base64
import json 
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
    

def main():

    model = "moondream:latest"
    prompt = "What is in this image?"

    adv_prompt = 'Analyze the image and return a JSON object containing the following information: ' + \
    '    { ' + \
    ' "objects": [ ' + \
    '{ + ' + \
    '  "name": "object name",+ ' \
    '  "count": number of instances, '+ \
    '  "description": "brief description" '+ \
    '} ' + \
    '], ' + \
    '"scene": "overall description of the scene", ' + \
    '"colors": ["dominant colors in the image"] ' + \
    '} ' + \
    ' Ensure the output is valid JSON format. ' 

    prompt = adv_prompt            
    url = "http://localhost:11434"
        
    image_inference = explain_image("../../docs/images/speech-inference.png", model, prompt, url)    
    print(image_inference)

if __name__ == "__main__":
    main()

