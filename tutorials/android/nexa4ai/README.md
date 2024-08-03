Nexa4AI


- Octopus_v4 - Graph paper - https://arxiv.org/pdf/2404.19296

- Run the model locally
    - Setup environment
        - python -m venv venv
        - source venv/bin/activate
        - pip install -r requirements.txt

    - Download model from hugging face
        - huggingface-cli download NexaAIDev/Octopus-v4
    - python octopus_v2.py

- GGUF model
    - Octopus-v4-Q4_0.gguf

        - llama.cpp
            - git clone https://github.com/ggerganov/llama.cpp --depth 1
            - cd llama.cpp
            - make
            - wget https://huggingface.co/NexaAIDev/octopus-v4-gguf/raw/main/Octopus-v4-Q4_0.gguf
            - ./llama-cli -m Octopus-v4-Q4_0.gguf -n 256 -p "<|system|>You are a router. Below is the query from the users, please call the correct function and generate the parameters to call the function.<|end|><|user|>Tell me the result of derivative of x^3 when x is 2?<|end|><|assistant|>"


        - Ollama - NOt used
        - git clone https://github.com/ollama/ollama.git ollama

        - wget https://huggingface.co/NexaAIDev/octopus-v4-gguf/raw/main/Octopus-v4-Q4_0.gguf

    - 
    - https://huggingface.co/NexaAIDev/octopus-v4-gguf
    - https://huggingface.co/NexaAIDev/gemma-2-2b-it-GGUF

- Octopus -v4 - Docker not working
    - docker pull nexaai/octopus4
    - docker run --gpus all -p 8700:8700 nexaai/octopus4
    - https://github.com/NexaAI/octopus-v4

- OctopusV2 model - 0.5B LLM
    - Model built on Gemma-2b, trained with function calling
    - https://huggingface.co/NexaAIDev/Octopus-v2

- Android Demo App
    - https://github.com/NexaAI/Ocotpus-v2-demo


    - [Download APK](https://public-storage.nexa4ai.com/android-demo-release/app-release.apk)
    - Connect Phone with USB debugger
    - adb install app-release.apk
    - https://huggingface.co/NexaAIDev/Octopus-v2-Android-Demo
    - Built on executorch - trained for small dataset

- [Demo Video](https://www.youtube.com/watch?v=tHQVVVZQzOM&list=PL4l1nVUEj_knXRu2k_Df35RwWYLnywZJ4&index=8)