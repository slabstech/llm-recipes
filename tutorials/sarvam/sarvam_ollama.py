import json
import requests
import os


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