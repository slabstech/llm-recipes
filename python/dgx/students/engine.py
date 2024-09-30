import requests
import json


def execute_prompt(url, prompt):



    #url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        #"model": "mistral",
        "model": "mistral-nemo",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    output = ""
    if response.status_code == 200:
        responses = response.text.strip().split('\n')
        for resp in responses:
            try:
                result = json.loads(resp)
                print(result.get('response', ''))
                output += result.get('response', '') + '\n'
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {resp}")

    else:
        print(f"Error: {response.status_code}")
    return output.strip()

def main():
    
    try:
        url = "http://10.2.0.7:11434/api/generate"
        prompt = "tell me a joke on mobile phone ?"
        execute_prompt(url, prompt)
    except FileNotFoundError:
        print("The file 'articles.json' was not found.")
    except json.JSONDecodeError:
        print("The file 'articles.json' is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")
    

if __name__ == "__main__":
    main()