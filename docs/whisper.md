Whisper - Speect to text model


- Docker - Start server
    - docker run -p 5000:5000 slabstech/whisper-api
    TODO 
    - CPU
        - docker run -p 5000:5000 slabstech/whisper-api-cpu
    - GPU
        - docker run -p 5000:5000 slabstech/whisper-api-gpu


- python python/whisper_api.py 
    - Replace the path the audio file
- Inference
    curl -F "file=@/path/to/filename.mp3" http://localhost:5000/whisper
        - Ex : curl -F "file=@/home/sachin/code/whisper/test1.flac" http://localhost:5000/whisper
{"results":[{"filename":"file","transcript":" What is your name? My name is Sachin."}]} 
    - You can test the API by sending a POST request to the route http://localhost:5000/whisper with a file in it. Body should be form-data.

- Run locally

- Clone Repo
  - git clone https://github.com/sachinsshetty/whisper.git
- Setup virtual environment
  - python -m venv venv
  - source venv/bin/activate
- Install whisper library
    - pip install -U openai-whisper
- Install ffmpeg
    - sudo apt update && sudo apt install ffmpeg
- Optional
    - pip install setuptools-rust
- Run whisper
    - whisper audio.flac audio.mp3 audio.wav --model medium

- Install sound recorder
    - sudo apt install gnome-sound-recorder


- Model
    - Small gives the nearest accurate answer with minimum resources.
        - small - 461 M
        - tiny - 71 M
        - base - 140 M


- python example
`
import whisper

model = whisper.load_model("small")
result = model.transcribe("audio.mp3")
print(result["text"])
`


- References
    - https://huggingface.co/NexaAIDev/Octopus-v2
    - moondream + octopus + phi-3
    - https://github.com/snakers4/silero-vad/tree/master/examples/microphone_and_webRTC_integration
    - https://hub.docker.com/r/onerahmet/openai-whisper-asr-webservice
    - https://github.com/ventz/whisper-openai-container
    - https://lablab.ai/t/whisper-api-flask-docker
    - https://github.com/lablab-ai/whisper-api-flask
    - https://github.com/meta-llama