Sarvam AI

Using local indic LLM

Use With Huggingface
    - HF Model -  https://huggingface.co/sarvamai/sarvam-2b-v0.5

        - python -m venv venv
        - source venv/bin/activate
        - pip install requirements-hf.txt
        - huggingface-cli download sarvamai/sarvam-2b-v0.5


        - python text_sarvam.py

    - Voice ASR - Shuka
    https://huggingface.co/sarvamai/shuka_v1

    - huggingface-cli download sarvamai/shuka_v1

    python voice_shuka.py


With Ollama
    - python -m venv venv
    - source venv/bin/activate
    - pip install requirements-ollama.txt
      
    - python sarvam_ollama.py



