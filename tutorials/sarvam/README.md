Sarvam AI

Using local indic LLM

- With Ollama
    - sarvam-2b 
        - Ollama - https://ollama.com/gaganyatri/sarvam-2b-v0.5
    - python -m venv venv
    - source venv/bin/activate
    - pip install requirements-ollama.txt

    - Download Model 
        -  python -m sarvam_ollama load_sarvam
    - Execute Code
        - python sarvam_ollama.py


- Use With Huggingface
    - sarvam-2b
        - HF Model -  https://huggingface.co/sarvamai/sarvam-2b-v0.5

        - python -m venv venv
        - source venv/bin/activate
        - pip install requirements-hf.txt
        - huggingface-cli download sarvamai/sarvam-2b-v0.5


        - python text_sarvam.py

    - Voice ASR - Shuka
        - HF Moel -https://huggingface.co/sarvamai/shuka_v1

        - huggingface-cli download sarvamai/shuka_v1

        - python voice_shuka.py



