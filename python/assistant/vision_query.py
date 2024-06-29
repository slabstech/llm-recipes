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

    model = "moondream"
    prompt = "What is in this image?"
            
    url = "http://localhost:11434"
        
    explain_image("../../docs/speech-inference.png", model, prompt, url)    

if __name__ == "__main__":
    main()

