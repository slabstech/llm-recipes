import requests

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
    ollama_url = "http://localhost:11434"
    model_name = "mistral"
    load_model( ollama_url, model_name )
    
if __name__ == "__main__":
    main()