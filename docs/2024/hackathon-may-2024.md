Hackathon - May 25-26, 2024

Replicate Figure 01 Robot - Speech to Speech Reasoning
All component running locally with OpenSource tools and OpenWeights models

Live Blog at X - https://x.com/gaganyatri/status/1794121114374828301

Hackathon Status
- Real-time data with locall LLM- mistral7b + function_calling [code - local_function_call_rest_api ](https://github.com/slabstech/llm-recipes/blob/main/src/mistral/local_function_call_rest_api.ipynb)


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
