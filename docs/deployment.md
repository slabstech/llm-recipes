Deployment 


Single container - Dockerfiles
1. Cpu only
2. Gpu only 

Monolithic build 
Call internal libs directly 

Full control of all components, 
Optimized for usability, 

Do performance optimization later after demo


Build 
1.whisper 
2. Coqui
3. Ollama 
4. Ffmpeg 

Download mistrak7b, whisper base , coqui - tachtron, voice clone 

Multi stage docker build

Build individual components and finally copy only build libraries to deploy image 

Use cpu and gpu separately  - 
Image name - speech-to-speech-cpu

 first cpu only, push to docker hub for docker compose .



Multi container -
Modify existing compose files for multi container support with gpu. Use the prebuilt binaries for gpu. Added additonal data after download and rebuild docker file. 
Save a checkpoint for immediate use.
