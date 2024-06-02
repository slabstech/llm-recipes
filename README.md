LLM Recipes

Demo's of LLM for Everyday use Run Locally

| Version |Concept | Tech | Status |
|---|---|---|---|
|v4| Image Generation + v3 | -- | Stable diffusion | 
|v3| Image/Scene Recognition + v2 | -- | llava/moondream | 
|v2| voice output + v1 | -- | tts| 
|v1| voice input + v1 | In progress | whisper + ffpmeg |
|v0|  [Text Query + API calls](python/api_interface.py)| Complete | mistral7B-v0.3 + ollama + RestAPI| 


Tutorials

- v2
    - Rest API + local LLM  
        - [local_function_call_rest_api.ipynb](tutorials/mistral/local_function_call_rest_api.ipynb) - function calling using mistral-inference and Mistral-7B-Instruct-v0.3
        - [ollama_mistral_function_calling.ipynb](tutorials/mistral/ollama_mistral_function_calling.ipynb) - function calling using ollama + mistral7b (4bit) + tokenizer.v3
        - GPT2 from scratch : [llm.c](https://github.com/karpathy/llm.c/discussions/481) 
        - Setup [Raspi + ollama + mistral7B + RestAPi](tutorials/raspi/README.md)
- v1
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
- v0
    - ChatUI  : ollama + open-webui + mistral-7B + docker
        - Setup + Documentation at [ollama-open-webui.md](docs/ollama-open-webui.md)
    - Code CoPilot : vscode + continue + ollama + mistral-7B
        - Setup document at [code-pair.md](docs/code-pair.md)

Extra 
 - [Clean install](docs/clean-ubuntu-setup.md) of ubuntu + docker + nvidia requirements
- Hackathon - [May 25-26, 2024](docs/2024/hackathon-may-2024.md) - Real time - browsing Capacity  - 
    -   Create function with Rest api endpoint detection 

    - !["Speech to Speech"](docs/speech-inference.png "Speech to Sppech")

