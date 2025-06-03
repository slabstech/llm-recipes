tensort RT - arm64

```bash
sudo apt-get update

sudo apt-get install -y git python3-pip libopenmpi-dev

sudo docker pull trystan/tensorrt_llm:aarch64-0.17.0.post1_90

sudo docker run --gpus all -it --rm --network=host --env NVIDIA_DRIVER_CAPABILITIES=all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 --name jetson_container_20250602_065549 trystan/tensorrt_llm:aarch64-0.17.0.post1_90

export HF_TOKEN=hf_your_tokn_ehere

python sample.py

// git clone https://github.com/NVIDIA/TensorRT-LLM.git

// cd TensorRT-LLM/examples/pytorch/


// meta-llama/Llama-3.2-1B-Instruct

// python quick_start.py


```

Reference
- https://github.com/NVIDIA/TensorRT-LLM/issues/3149
- https://github.com/dusty-nv/jetson-containers
- https://github.com/NVIDIA/TensorRT-LLM.git
- https://github.com/NVIDIA/TensorRT-LLM.git
- https://github.com/NVIDIA/TensorRT-LLM/tree/main/examples/pytorch
- https://github.com/NVIDIA/TensorRT-LLM/blob/main/examples/pytorch/quickstart_multimodal.py#L107

- pip install --upgrade tensorrt_llm --extra-index-url https://pypi.nvidia.com
- https://lambda.ai/lambda-stack-deep-learning-software