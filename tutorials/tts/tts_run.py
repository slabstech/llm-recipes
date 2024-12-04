import requests

# Define the API endpoint
url = "http://localhost:5002/api/tts"

# Prepare your request payload
data = {
    "text": "Hello, this is a test of Coqui TTS!",
    "model": "tts_models/en/ljspeech/tacotron2",
    "speaker_idx": 0  # Optional, depending on your model
}

# Send POST request to the TTS server
response = requests.post(url, json=data)

# Check if the request was successful
if response.status_code == 200:
    # Save the audio file
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("Audio saved as output.wav")
else:
    print("Error:", response.status_code, response.text)
