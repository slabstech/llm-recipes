Mistral 

- Running inference and function calling
    - python -m venv venv
    - source venv/bin/activate
    - pip install mistral-inference
    - export MISTRAL_MODEL=$HOME/mistral_models
    - mkdir -p $MISTRAL_MODEL
    - export M7B_DIR=$MISTRAL_MODEL/7B_instruct
    - wget https://models.mistralcdn.com/mistral-7b-v0-3/mistral-7B-Instruct-v0.3.tar
    - mkdir -p $M7B_DIR
    - tar -xf mistral-7B-Instruct-v0.3.tar -C $M7B_DIR

- Ollama raw Mode
    - `curl http://localhost:11434/api/generate -d '{
  "model": "mistral:7b",
  "prompt": "[INST] why is the sky blue? [/INST]",
  "raw": true,
  "stream": false
}'` 

    - `curl http://localhost:11434/api/generate -d '{
  "model": "mistral:7b",
  "prompt": "[AVAILABLE_TOOLS] [{\"type\": \"function\", \"function\": {\"name\": \"get_current_weather\", \"description\": \"Get the current weather\", \"parameters\": {\"type\": \"object\", \"properties\": {\"location\": {\"type\": \"string\", \"description\": \"The city and state, e.g. San Francisco, CA\"}, \"format\": {\"type\": \"string\", \"enum\": [\"celsius\", \"fahrenheit\"], \"description\": \"The temperature unit to use. Infer this from the users location.\"}}, \"required\": [\"location\", \"format\"]}}}][/AVAILABLE_TOOLS] [INST] What is the weather like today in San Francisco [/INST]",
  "raw": true,
  "stream": false
}'` 


- HF
  - pip install --upgrade huggingface_hub
  - mkdir 7B-Instruct-v0.3
  - mkdir -p ~/.cache/huggingface
  - sudo chown -R $USER ~/.cache/huggingface
  - sudo chmod -R 755 ~/.cache/huggingface
  - Copy token from https://huggingface.co/settings/tokens
  - huggingface-cli login

- Reference
    - https://github.com/mistralai/mistral-inference
    - https://github.com/ollama/ollama/blob/main/docs/api.md#request-raw-mode
    - https://ollama.com/library/mistral
    - https://www.youtube.com/watch?v=YJeJiSWgtlE
    - https://github.com/mistralai/cookbook/blob/main/function_calling.ipynb
