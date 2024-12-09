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

    

