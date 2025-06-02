tensort RT - arm64

sudo apt-get update

sudo apt-get install -y git python3-pip libopenmpi-dev



sudo docker pull trystan/tensorrt_llm:aarch64-0.17.0.post1_90


 sudo docker run --gpus all -it --rm --network=host --env NVIDIA_DRIVER_CAPABILITIES=all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 --name jetson_container_20250602_065549 trystan/tensorrt_llm:aarch64-0.17.0.post1_90



git clone https://github.com/NVIDIA/TensorRT-LLM.git

 cd TensorRT-LLM/examples/pytorch/


python quick_start.py

Reference

- https://github.com/dusty-nv/jetson-containers
- https://github.com/NVIDIA/TensorRT-LLM.git
- https://github.com/NVIDIA/TensorRT-LLM.git
- https://github.com/NVIDIA/TensorRT-LLM/tree/main/examples/pytorch
- https://github.com/NVIDIA/TensorRT-LLM/blob/main/examples/pytorch/quickstart_multimodal.py#L107
