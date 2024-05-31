Setup  with RaspberryPi


add to bash 
export OLLAMA_ENDPOINT='http://gpu-server:11434'


- Create virtual environment
    - python -m venv venv
    - source venv/bin/activate
- Install required libraries
    - pip install -r requirements.txt  # pip install ollama pandas mistral-common