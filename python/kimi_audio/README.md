Kimi Audio

```bash
cd speech-to-speech
python3 -m venv venv
source venv/bin/activate
pip install -r requriements.txt
python main.py
```

- https://github.com/MoonshotAI/Kimi-Audio
- https://github.com/MoonshotAI/Kimi-Audio-Evalkit



- Tiny Whisper

git clone https://github.com/morioka/tiny-openai-whisper-api.git
cd tiny-openai-whisper-api
 python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
export WHISPER_MODEL=turbo

uvicorn main:app --host 0.0.0.0

curl --request POST http://127.0.0.1:8000/v1/audio/transcriptions \
  -F model="whisper-1" \
  -F file="@english_sample.wav"


curl --request POST http://127.0.0.1:8000/v1/audio/transcriptions \
  -F model="whisper-1" \
  -F file="@kannada_sample.wav"
