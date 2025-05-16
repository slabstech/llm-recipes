dwani.ai - gh200


ASR - https://github.com/dwani-ai/asr-indic-server.git

TTS - https://github.com/dwani-ai/tts-indic-server.git

Docs - https://github.com/dwani-ai/docs-indic-server.git

Translate

LLM

dwani-server 


To use pytorch on 
python -m venv --system-site-packages venv




curl -X POST http://lambda-sip:7860/v1/chat/completions -H "Content-Type: application/json" -d '{
  "model": "gemma-3-12b-it-Q8_0.gguf",
  "messages": [
    {"role": "user", "content": "Hello, who are you?"}
  ]
}'


---

