Ontogpt 

- Setup
    - Create virtual environment
        - python3.10 -m venv venv
        - source venv/bin/activate
    - Install ontogpt
        - pip install ontogpt
    - Create api-key to use with ollama
        - runoak set-apikey -e openai hello-world
    - Start ollama server 

- Execute Commands
    - echo "One treatment for high blood pressure is carvedilol." > example.txt
    - ontogpt extract -i example.txt -t drug --model ollama/llama3.2

    
- web-ontogpt   
    - pip install ontogpt[web]
    - web-ontogpt

    - update file src/ontogpt/webapp/main.py
        - provide proper version names for ollama model
            - ollama/llama3.2
            - ollama/llama3.1
    
    - pip install poetry
    - poetry build
    - poetry install -E web
    - poetry run web-ontogpt
