LLM Recipes

Hackathon - May 25-26, 2024

Replicate Figure 01 Robot - Speech to Speech Reasoning
All component running locally with OpenSource tools and OpenWeights models

Live Blog at X - https://x.com/gaganyatri/status/1794121114374828301

In Scope - 
1. Scene/Image description
2. Voice to Text  - conversion
3. Text Q & A with Live Data Fetch
4. Text to Voice

Out of Scope - Humanoid Robot

---
Status

What is currently in progress ?
- Real Time info interface to Mistral7B model

What is completed ?

What needs to be done ?

---
llm-recipes - path to Jarvis 

What does the repo contain ? 
Steps with code to run a llm model locally with below capability 
- ChatBot UI - openweb-ui + ollama + docker 

WIP 
- RealTime data- mistral7b + function_calling interface + vllm 

Future 

4. Voice to text - whisper ??
5. Text to voice - eleven labs ??
6. Image to text - llava 
7. Text to image - stable diffusion 
8. Gpt assistant- RAG ? / fune tuning 


Constraints -

1. System requirements  -
Minimum 20GB vram for inference, mistral 7B is 16GB at full precision ,
 query 
32k context window x 16bits = ?? 

Solution - quantize to 4bits = 4 GB +


2. Deployment 
Vllm deployment with docker 
Need to experiment to find clean docker compose 

3. Real time - browsing Capacity // perplexity clone ??
Create function with Rest api endpoint detection 
Summarise website info into required format. 

---

Usage of LLM for Everyday use

- v1
    - Prompt Optimization - DSPy + Mixtral + Ollama/Mistral API
        - Docs at [docs/dspy.md](https://github.com/slabstech/llm-recipes/blob/main/docs/dspy.md)
        - Code examples at [src/dspy](https://github.com/slabstech/llm-recipes/tree/main/src/dspy)
    - Agents : autogen + vllm + gemma
        - [VLLM setup](https://github.com/slabstech/llm-recipes/blob/main/docs/vllm.md) 
    - Agents : autogen + ollama + gemma
        - Setup + Documentation at [docs/2024/agent-code.md](https://github.com/slabstech/llm-recipes/blob/main/docs/2024/agent-code.md) 
        - Code examples at [src/autogen](https://github.com/slabstech/llm-recipes/tree/main/src/autogen)
        - Output from examples at [docs/2024/agent-example-output.md](https://github.com/slabstech/llm-recipes/blob/main/docs/2024/agent-example-output.md)
    - llama.cpp + Raspi 4
        - [Docs](https://github.com/slabstech/llm-recipes/blob/main/docs/llama-cpp.md) for setup of Raspi 4 inference. 
- v0
    - ChatUI  : ollama + open-webui + mistral-7B + docker
        - Setup + Documentation at [docs/ollama-open-webui.md](https://github.com/slabstech/llm-recipes/blob/main/docs/ollama-open-webui.md)
    - Code CoPilot : vscode + continue + ollama + mistral-7B
        - Setup document at [docs/code-pair.md](https://github.com/slabstech/llm-recipes/blob/main/docs/code-pair.md)

Extra 
 - [Clean install](https://github.com/slabstech/llm-recipes/blob/main/docs/clean-ubuntu-setup.md) of ubuntu + docker + nvidia requirements
 