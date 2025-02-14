
Run Speech to text 

`
- docker compose -f python/docker-compose.yml up -d
- docker ps
    - find container-id of ollama
- docker exec -it <container_id_or_name> /bin/bash
    - ollama pull mistral:7b
- create virtual environment
    - python -m venv venv
    - source venv/bin/activate
    - pip install -r requirements.txt
    
- python python/api_interface.py
- python python/whisper_api.py
`


https://github.com/huggingface/speech-to-speech