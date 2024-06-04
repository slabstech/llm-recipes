import requests

url = "http://localhost:5000/whisper"
#files = {'file': open('/path/to/filename.mp3', 'rb')}
files = {'file': open('/home/sachin/code/whisper/test1.flac', 'rb')}
response = requests.post(url, files=files)

if response.status_code == 200:
    print("File uploaded successfully!")
    print(response.text)
else:
    print(f"Error: {response.status_code} - {response.text}")
