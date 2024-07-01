import json 
import requests
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

    metadata_file_name = metadata_file_name.replace('.json', '')

    insight_file_name = f'{metadata_file_name}_insight.json' 
    # Open the file in append mode ('a')
    with open(insight_file_name, 'a') as file:
    # Write the response data to the file
        file.write(str(response_data))
    return insight_file_name
 