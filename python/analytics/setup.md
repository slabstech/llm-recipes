Setup

- Create virtual environment and install libraries
  - python -m venv venv
  - source venv/bin/activate
  - pip install -r requirements.txt

- Setup ollama
  - docker compose up -d llm-compose.yml
    - ollama pull deepseek-r1:7b
    - ollama pull qwen2.5


- Run the PDF parser and create data for TTS input
  - python pdf-parser.py

- Send data to TTS