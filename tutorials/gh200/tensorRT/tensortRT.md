TensorRT-LLM

sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt update

sudo apt install python3.12

sudo update-alternatives --install /usr/bin/python3 

python3 /usr/bin/python3.12 2

sudo update-alternatives --install /usr/bin/python3 

python3 /usr/bin/python3.10 1

sudo apt install python3.12-venv


python -m venv --system-site-packages venv

pip install --upgrade pip setuptools wheel

 pip3 install torch==2.7.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

 sudo apt-get -y install libopenmpi-dev && pip3 install --upgrade pip setuptools && pip3 install tensorrt_llm


----

apt-get update && apt-get -y install python3.10 python3-pip openmpi-bin libopenmpi-dev




pip3 install tensorrt_llm -U --pre --extra-index-url https://pypi.nvidia.com

python3 -c "import tensorrt_llm"

https://developer.nvidia.com/blog/optimizing-inference-on-llms-with-tensorrt-llm-now-publicly-available/