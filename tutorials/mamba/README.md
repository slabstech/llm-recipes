Codestral Mamba

Using Transformers

pip install -U "huggingface_hub[cli]"
huggingface-cli login --token $HF_TOKEN
huggingface-cli download 'mistralai/Mamba-Codestral-7B-v0.1' --local-dir codestral-7B --revision="refs/pr/9" --exclude consolidated.safetensors
pip install transformers torch sentencepiece protobuf


python codestral-mamba.py


- Run with continue

- Setup
  - mistral-inference
    - python3.10 -m venv venv
    - source venv/bin/activate
    - pip install mistral-inference
    - pip install wheel
    - pip install --upgrade pip
    - pip install packaging mamba-ssm causal-conv1d transformers
    - 
    - pip install -U "huggingface_hub[cli]"
    - huggingface-cli login --token $HF_WRTE
    - huggingface-cli download mistralai/Mamba-Codestral-7B-v0.1
    - https://github.com/mistralai/mistral-inference
    - export CODESTRAL_MAMBA=/home/ssf79/.cache/huggingface/hub/models--mistralai--Mamba-Codestral-7B-v0.1/snapshots/d4521ac4b7658f796233ce47e8e695933f3cd48a
    - mistral-chat $CODESTRAL_MAMBA --instruct --max_tokens 256



pip install -U "huggingface_hub[cli]"
huggingface-cli login --token $HF_TOKEN
huggingface-cli download 'mistralai/Mamba-Codestral-7B-v0.1' --local_dir . --revision="refs/pr/9" --exclude consolidated.safetensors
pip install transformers torch



    - With vllm
	- pip install vllm
	- python -u -m vllm.entrypoints.openai.api_server \
       --host 0.0.0.0 \
       --model mistralai/Mamba-Codestral-7B-v0.1
  
    - vllm image build
	- git clone https://github.com/mistralai/mistral-inference.git
 	- docker build deploy --build-arg MAX_JOBS=8

  - https://mistral.ai/news/codestral-mamba/
  - https://docs.vllm.ai/en/latest/models/supported_models.html
  - https://huggingface.co/mistralai/Mamba-Codestral-7B-v0.1
  - https://github.com/NVIDIA/TensorRT-LLM/tree/main/examples/mamba
  - https://developer.nvidia.com/blog/revolutionizing-code-completion-with-codestral-mamba-the-next-gen-coding-llm/

  - Paper
    - Mamba 1 - https://arxiv.org/abs/2312.00752
    - Mamba 2 - https://arxiv.org/pdf/2405.21060




- Milestones
  - Learn how to utilise CUDA kernels
  - Implement mamba2 from scratch to run codestral locally

  - Make it compatible with llama.cpp and later to ollama


- Reference
  - https://mistral.ai/news/codestral-mamba/
  - mamba - research - https://arxiv.org/abs/2312.00752 
  - https://huggingface.co/mistralai/mamba-codestral-7B-v0.1
  - https://github.com/NVIDIA/TensorRT-LLM/tree/main/examples/mamba
  - https://github.com/state-spaces/mamba
  - https://github.com/NVIDIA/TensorRT-LLM/tree/main/examples/mamba


