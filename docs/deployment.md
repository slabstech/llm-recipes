Deployment 

Docker compose with two ollama containers.
Using the same volume for data/image reuse

* Experiment 
  - multiome model load with single container - MAX_NUM_MODELS
  - Use two containers for mistral7b and moondream

* Write a script which analyse memory availability through nvidia-smi and starts containers as accordingly

-- 
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

- Reference
    - Docker - Whisper X
        - https://github.com/jim60105/docker-whisperX
        - https://github.com/ahmetoner/whisper-asr-webservice/blob/main/docker-compose.gpu.yml
        - https://github.com/jim60105/docker-whisperX/blob/master/Dockerfile