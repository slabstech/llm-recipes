Raspi Module


Installation steps 
- sudo apt update && sudo apt install git
- sudo apt-get install git-lfs
- git lfs install
- mkdir piRun
- cd piRun
- python -m venv env
- source env/bin/activate

- python3 -m pip install torch numpy sentencepiece
- sudo apt install g++ build-essential

- wget https://github.com/ggerganov/llama.cpp/archive/refs/heads/gg/phi-2.zip
- unzip phi-2.zip 
- rm phi-2.zip


- cd llama.cpp-gg-phi-2/
- make 

- mkdir phi-2-gguf/
- pip install -U huggingface_hub
- huggingface-cli download TheBloke/phi-2-GGUF --local-dir phi-2-gguf/  

./main -m phi-2-gguf/phi-2.Q4_K_M.gguf -p "Question: Write a python function to print the first n numbers in the fibonacci series"




Alternate Steps for gguf model build from source


- Download - https://huggingface.co/microsoft/phi-2
- pip install -U huggingface_hub
- huggingface-cli download microsoft/phi-2


- python convert-hf-to-gguf.py phi-2

./main -m phi-2/ggml-model-f16.gguf -p "Question: Write a python function to print the first n numbers in the fibonacci series"

-- model Deployment

./main -m models/phi-2.Q4_0.gguf -p "Question: Write a python function to print the first n numbers in the fibonacci series"


Reference
- https://www.dfrobot.com/blog-13498.html

- Docker on Raspi - https://docs.docker.com/engine/install/debian/
- https://huggingface.co/TheBloke/phi-2-GGUF
- https://ubuntu.com/blog/deploying-open-language-models-on-ubuntu