Triton Server Setup

Build Triton
    - git clone https://github.com/triton-inference-server/server
    - cd server
    - python build.py  

Build Mixtral with Tensor RT-LLM

    - git clone https://github.com/NVIDIA/TensorRT-LLM/
    - cd TensorRT-LLM
    - cd examples/mixtral
    - pip install -r requirements
    - git lfs install
    - git clone https://huggingface.co/mistralai/Mixtral-8x7B-v0.1


- Build Triton
    - https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/customization_guide/build.html
- Security
    - https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/customization_guide/deploy.html
    - https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/customization_guide/build.html#building-with-docker

- build mixtral
    - https://github.com/NVIDIA/TensorRT-LLM/blob/main/examples/mixtral/README.md
- https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/getting_started/quickstart.html
- Build mistral - https://github.com/NVIDIA/TensorRT-LLM/tree/main/examples/llama#mistral-v01


Extra 
- sudo useradd -m llm
- sudo passwd llm
- sudo usermod -aG sudo llm
 - apt install python3.10-venv
 - apt install python3-pip
 - sudo apt-get install build-essential linux-generic libmpich-dev libopenmpi-dev
 - sudo apt install openmpi-devel