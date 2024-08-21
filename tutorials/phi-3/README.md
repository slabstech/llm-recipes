Phi-3

- Setup 
  - python -m venv venv
  - source venv/vbin/activate
  - pip install requirements.txt

Text
- Ollama
  - ollama run phi3.5
  - python phi_text_ollama.py

- Huggingface
  - huggingface_cli download microsoft/Phi-3.5-mini-instruct
   - python phi_text_hf.py

Vision 
- Huggingface
  - huggingface_cli download microsoft/Phi-3.5-vision-instruct
  - python phi_vision_hf.py




Vision

- Reference
  - https://huggingface.co/microsoft/Phi-3.5-vision-instruct
  - https://github.com/microsoft/Phi-3CookBook/blob/main/md/04.Fine-tuning/FineTuning_Vision.md
