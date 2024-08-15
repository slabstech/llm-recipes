import json
import requests
import os

def download_sarvam():
    ollama_url = "http://localhost:11434"
    model_name = "gaganyatri/sarvam-2b-v0.5"
    load_model( ollama_url, model_name )

def load_model(ollama_url, model_name):
    command = "/api/pull"
    url = ollama_url + command
    model = model_name + ":latest"
    payload = {"name": model}
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("Request successful!")
        print(response.text)
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)

def main():
    prompt = "ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ " 

    model = "gaganyatri/sarvam-2b-v0.5"
    
    ollama_endpoint = 'http://localhost:11434/api/generate'

    response = requests.post(ollama_endpoint,
                      json={
                          'model': model,
                          'prompt': prompt,
                          'stream':False,
                      }, stream=False
                      )
    
    response.raise_for_status()
    result = response.json()

    print(result)

if __name__ == "__main__":
    main()