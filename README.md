Assistant

On-device assistant with Speech, Vision, Text search
 

!["Multi-modal On-device"](docs/images/on-device.drawio.png "Multi-modal On-device") 

| Version |Concept | Tech | Status |
|---|---|---|---|
|v0.6| Image Generation + v0.4 | -- | Stable diffusion | 
|v0.5| Mobile Interface + v0.4 | -- | Android App + local server | 
|v0.4| [Image/Scene Recognition + v0.3](assistant/assitant-tutorial.ipynb) | In progress | llava/moondream | 
|v0.3| [Speech output + v0.2](assistant/speech-to-speech-inference.py) | Complete | coqui tts + v1 | 
|v0.2| [Speech input + v0.1](assistant/voice_api_interface.py) | Complete | whisper + ffpmeg + v0 |
|v0.1| [Text Query + API calls](assistant/api_interface.py)| Complete | mistral7B-v0.3 + ollama + RestAPI| 


Demo's of LLM for Everyday use Run Locally

- [Alexa/Siri/Google](https://www.youtube.com/watch?v=UqS3NxJ2L_I) Voice Commands - [Example](assistant/speech-to-speech-inference.ipynb)
- [Figure 01](https://www.youtube.com/watch?v=Sq1QZB5baNw) Robot Demo- [Example](assistant/assitant-tutorial.ipynb)
- Ipad Calculator App - Example


Tutorials
- v3
    - Vision /Image Recognition
        - [vision-search.ipynb](tutorials/vision/vision-search.ipynb) : moondream2/llava + ollama
- v2
    - Voice Output + v1
        - [speech-to-speech-inference.ipynb](assistant/speech-to-speech-inference.ipynb) - Coqui tts + voice clone
            - [Speech to Speech Inference Demo](docs/demo-speech-to-speech-inference.md)
- v1
    - Voice Input + v0
        - [aws-bedrock-mistral-whisper.ipynb](tutorials/mistral/aws-bedrock-mistral-whisper.ipynb) - Whisper + AWS Bedrock + Mistral + RestAPI
- v0
    - Rest API + local LLM  
        - [local_function_call_rest_api.ipynb](tutorials/mistral/local_function_call_rest_api.ipynb) - function calling using mistral-inference and Mistral-7B-Instruct-v0.3
        - [ollama_mistral_function_calling.ipynb](tutorials/mistral/ollama_mistral_function_calling.ipynb) - function calling using ollama + mistral7b (4bit) + tokenizer.v3
        - [aws-bedrock-mistral.ipynb](tutorials/mistral/aws-bedrock-mistral.ipynb)AWS Bedrock + Mistral Large + Function call
- Base Setup
    - ChatUI  : ollama + open-webui + mistral-7B + docker
        - Setup + Documentation at [ollama-open-webui.md](docs/ollama-open-webui.md)
    - Code CoPilot : vscode + continue + ollama + mistral-7B
        - Setup document at [code-pair.md](docs/code-pair.md)

Extra 
 - Mobile Interface - Android Multi-modal app search
    - []
 - [Clean install](docs/clean-ubuntu-setup.md) of ubuntu + docker + nvidia requirements
 - Experiments
    - GPT2 from scratch : [llm.c](https://github.com/karpathy/llm.c/discussions/481) 
    - Setup [Raspi + ollama + mistral7B + RestAPi](tutorials/raspi/README.md)
    - Prompt Optimization - DSPy + Mixtral + Ollama/Mistral API
        - Docs at [dspy.md](docs/dspy.md)
        - Code examples at [dspy](tutorials/dspy)
    - Agents : autogen + vllm + gemma
        - [VLLM setup](docs/vllm.md) 
    - Agents : autogen + ollama + gemma
        - Setup + Documentation at [agent-code.md](docs/2024/agent-code.md) 
        - Code examples at [autogen](tutorials/autogen)
        - Output from examples at [agent-example-output.md](docs/2024/agent-example-output.md)
    - llama.cpp +  Phi model
        - [Docs](docs/llama-cpp.md) for setup of Phi model inference. 

- Hackathon - [May 25-26, 2024](docs/2024/hackathon-may-2024.md) - Real time - browsing Capacity  - 
    -   Create function with Rest api endpoint detection 

