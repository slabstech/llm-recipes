import requests

def load_model(ollama_url, model_name):

    # Check if model is already available
    command = "/api/tags"
    url = ollama_url + command
    response = requests.get(url)
    models = response.json()["models"]

    # Check if the model is in the list of available models
    model_found = False
    for model in models:
        if model["name"] == model_name:
            model_found = True
            break

    if model_found:
        print(f"Model {model_name} is already available.")
    else:
        command = "/api/pull"
        url = ollama_url + command
        payload = {"name": model_name}
        
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
    model_name = "mistral:latest"
    load_model( ollama_url, model_name )
    
if __name__ == "__main__":
    main()