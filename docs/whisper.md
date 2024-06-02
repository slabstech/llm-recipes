Whisper - Speect to text model


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