Nexa4AI


- Run the model locally
    - Setup environment
        - python -m venv venv
        - source venv/bin/activate
        - pip install -r requirements.txt

    - Download model from hugging face
        - huggingface-cli download NexaAIDev/Octopus-v4
    - python octopus_v2.py


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