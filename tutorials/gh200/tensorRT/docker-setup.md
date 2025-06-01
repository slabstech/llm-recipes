tensorRT-LLM with docker

uname -a  >> aarch64

sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install -y curl
distribution=$(. /etc/os-release; echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

sudo docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi

sudo apt-get install -y python3.10 python3-pip openmpi-bin libopenmpi-dev git git-lfs wget

pip3 install --upgrade pip setuptools

sudo docker pull nvcr.io/nvidia/pytorch:25.01-py3

// sudo docker run --rm --runtime=nvidia --gpus all --entrypoint /bin/bash -it -v $HOME:/workspace nvcr.io/nvidia/pytorch:25.01-py3

sudo docker run --rm  --gpus all --entrypoint /bin/bash -it -v $HOME:/workspace nvcr.io/nvi
dia/pytorch:25.01-py3

// pip3 install tensorrt_llm==0.8.0 -U --extra-index-url https://pypi.nvidia.com

---  Inside docker container
pip3 install numpy torch transformers huggingface_hub
pip3 install --upgrade pip setuptools
pip3 install tensorrt_llm -U --extra-index-url https://pypi.nvidia.com --verbose

python3 -c "import tensorrt; print(tensorrt.__version__)"

pip3 uninstall tensorrt -y

pip install tensorrt

python3 -c "import tensorrt; print(tensorrt.__version__)"


---

git clone https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0 gpt2
cd gpt2
wget -q https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0/resolve/main/pytorch_model.bin
cd ..


git clone --branch v0.8.0 https://github.com/NVIDIA/TensorRT-LLM.git
cd TensorRT-LLM
python3 examples/gpt/hf_gpt_convert.py -i gpt2 -o ./c-model/gpt2 --tensor-parallelism 1 --storage-type float16

