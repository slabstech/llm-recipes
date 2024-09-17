LLM Recipes

- Assistant
    - On-device assistant with Speech, Vision, Text search
 

!["Multi-modal On-device"](docs/images/on-device.drawio.png "Multi-modal On-device") 



| Version |Concept | Tech | Status |
|---|---|---|---|
|v0.8| [Quantisation](tutorial/llama.cpp/) | In progress | llama.cpp  | 
|v0.7| [On-device Mobile](tutorial/android/) | In progress | Android + TF lite  | 
|v0.6| [UI](UI) | In progress | Typescript | 
|v0.5| [Indoor Maps + v0.4](python/reconaissance/reconaissance.py) | In progress | ROS2  | 
|v0.4| [Image/Scene Recognition + v0.3](python/assistant/vision_query.py) | complete | llava/moondream | 
|v0.3| [Speech output + v0.2](python/assistant/speech-to-speech-inference.py) | Complete | coqui tts + v1 | 
|v0.2| [Speech input + v0.1](python/assistant/voice_api_interface.py) | Complete | whisper + ffpmeg + v0 |
|v0.1| [Text Query + API calls](python/assistant/api_interface.py)| Complete | mistral7B-v0.3 + ollama + RestAPI| 

- Base Setup
    - ChatUI  : ollama + open-webui + mistral-7B + docker
        - Setup + Documentation at [ollama-open-webui.md](docs/ollama-open-webui.md)
    - Code CoPilot : vscode + continue + ollama + mistral-7B
        - Setup document at [code-pair.md](docs/code-pair.md)

- [Tutorials](docs/tutorials.md)

- Extra 
    - [Clean install](docs/clean-ubuntu-setup.md) of ubuntu + docker + nvidia requirements

- Applications 
    - Reconnaisance with Drone
    - Use Drones to create real-time insights of Warehouse, Home securiy


!["Reconassiance"](python/reconaissance/reconaissance.drawio.png "Reconaissance")

- Upcoming Challenges
    - Wanddb - HAckerCup - [Oct 16](https://github.com/wandb/aihackercup)
    - Nvidia Hack AI -[Oct 3](https://hackaichallenge.devpost.com/)