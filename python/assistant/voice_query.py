import json
import requests

def voice_query(file_name):
    url = "http://localhost:5000/whisper"
    files = {'file': open(file_name, 'rb')}
    response = requests.post(url, files=files)

    response_query = ""
    if response.status_code == 200:
        query = json.loads(response.text)
        for result in query['results']:
            transcript = result['transcript']
            response_query = response_query + transcript
        return response_query    
    else:
        print(f"Error: {response.status_code} - {response.text}")

def main():
    file_name = 'output.wav'
    voice_query(file_name=file_name)

if __name__ == "__main__":
    main()
