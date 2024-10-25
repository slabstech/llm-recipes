Sarvam AI

Using local indic LLM

- sarvam-1
    - https://huggingface.co/sarvamai/sarvam-1
    - [Collab Demo](https://colab.research.google.com/drive/1nGstaG4grFdUvLFdKCrBSq5UAZBoUO32?usp=sharing)


- With Ollama
    - sarvam-2b 
        - Ollama - https://ollama.com/gaganyatri/sarvam-2b-v0.5
    - python -m venv venv
    - source venv/bin/activate
    - pip install -r requirements-ollama.txt

    - Download Model 
        -  python -m sarvam_ollama load_sarvam
    - Execute Code
        - python sarvam_ollama.py

- Prequisities
    - ollama should be running on Docker
        - For CPU
            - docker compose -f cpu-ollama.yml up -d
        - For GPU
            - docker compose -f gpu-ollama.yml up -d

- Use With Huggingface
    - sarvam-2b
        - HF Model -  https://huggingface.co/sarvamai/sarvam-2b-v0.5

        - python -m venv venv
        - source venv/bin/activate
        - pip install -r requirements-hf.txt
        - huggingface-cli download sarvamai/sarvam-2b-v0.5


        - python text_sarvam.py

    - Voice ASR - Shuka
        - HF Model -https://huggingface.co/sarvamai/shuka_v1
        - python -m venv venv
        - source venv/bin/activate
        - pip install -r requirements-shuka.txt
        - huggingface-cli download sarvamai/shuka_v1

        - python voice_shuka.py


- Shuka with ollama ?


- Is built on https://huggingface.co/fixie-ai/ultravox-v0_3

