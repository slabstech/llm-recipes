import httpx

with open('jfk.wav', 'rb') as f:
    files = {
        'file': ('jfk.wav', f),
        #'model': (None, 'Systran/faster-whisper-large-v3')
        'model': (None, 'Systran/faster-whisper-small')  # or the model name required by the API
    }
    response = httpx.post('http://whisper-server:8000/v1/audio/transcriptions', files=files)

print(response.text)
