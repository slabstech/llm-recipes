Version 1

- Upload image for vegetables/ fruit.
- Provide prompt for research
	- Identify if box contains rotten items
- Result - highlight box to moved


Framework

- Frontend - React PWA using Typescript / Vite
- Backend - Ollama inference with Docker 
  - Python with flask for Additional Prompt Optimisation

Run time 
 - docker compose file with ollama and frontend
	

- Frontend - 

- Single Page
  - Image upload modal
  - Prompt text box
  - Process button
  - Result text box


- Reference
  - openweb-ui like for frontend


- TODO
  - July 18
    - Add Progress Bar - For LLM process and reply - Dont Stream
    - Add model status bar - currently downloaded model, switch model via dropdown
    - First Start - Show progress for default model download
  - July Week 3
    - Text only - mistral
    - Image + Text - Lllava/moondream + mistral
    - Connect to synthetic API/ERP via function call to get status of items
  
- V2
 - Text For Enhanced User / Supervisor or Manager

- v3 
 - Voice Query for real time
 - Connect with handsfree headset to get Info - For floor Workers


Business case - 
Automated Orders 

Handsfree - query system with whisper and Function api

Using whisper- 
Worker can request next task.  Can be integrated with their headset . 
Usable in major languages

Inside Supermarket 

Instructions wil be given based on System state. 
If any item is over on shelf, provide notification to floor worker to replinesh stock


1. We can use function calling
To map their api, 

2. From images - we can find what items are b over .


-- 

Elevator Pitch

Real-time identification of Vegetable/Fruits status to eliminate waste due to contamination.  

Intelligent Hands-free system connected to existing Headset, Instructions will be given based on System state. If any item is over on shelf, provide notification to floor worker to replenish stock.
Warehouse Mapping with multimodal LLM using CCTV cameras.

---

Create time series for CCTC tracking

check llava rotten status with json response, 
Find the quantity of images, with small images
