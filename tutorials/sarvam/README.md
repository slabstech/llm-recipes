Sarvam AI


Using local indic LLM

HF Model -  https://huggingface.co/sarvamai/sarvam-2b-v0.5

- python -m venv venv
- source venv/bin/activate
- pip install requirements.txt
- huggingface-cli download sarvamai/sarvam-2b-v0.5


python text_sarvam.py

- Voice ASR - Shuka
https://huggingface.co/sarvamai/shuka_v1

- huggingface-cli download sarvamai/shuka_v1

python voice_shuka.py



- Create ollama model
    - ollama create sarvam-2b -f Modelfile
    - ollama cp sarvam-2b gaganyatri/sarvam-2b-v0.5
    - ollama push gaganyatri/sarvam-2b-v0.5


- Setup ssh-key from ollama
    - sudo cat /usr/share/ollama/.ollama/id_ed25519.pub
    - https://ollama.com/settings/keys