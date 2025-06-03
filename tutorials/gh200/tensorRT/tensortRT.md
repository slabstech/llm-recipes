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


python3.10 -m venv --system-site-packages venv

pip3 install tensorrt_llm -U --pre --extra-index-url https://pypi.nvidia.com

python3 -c "import tensorrt_llm"

https://developer.nvidia.com/blog/optimizing-inference-on-llms-with-tensorrt-llm-now-publicly-available/


-- 

sudo apt-get update
sudo apt-get install libssl-dev


wget https://github.com/Kitware/CMake/releases/download/v4.0.2/cmake-4.0.2.tar.gz

tar xzf cmake-4.0.2.tar.gz 

cd cmake-4.0.2

./configure --prefix=/opt/cmake


make

sudo make install
--

sudo apt-get update && sudo apt-get -y install git git-lfs

git lfs install

git clone https://github.com/NVIDIA/TensorRT-LLM.git

cd TensorRT-LLM

sudo apt-get update

sudo apt-get install python3-distutils

python3.10 -m venv venv

source venv/bin/activate
python3 ./scripts/build_wheel.py --cuda_architectures "90-real"


-- 
only python code

TRTLLM_USE_PRECOMPILED=1 pip wheel . --no-deps --wheel-dir ./build
pip install ./build/tensorrt_llm*.whl


pip install ./build/tensorrt_llm*.whl


