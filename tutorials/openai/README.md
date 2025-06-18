openai - API


- Setup Project
    ```bash
    python3.10 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
- Terminal 1
    ```bash
    sudo docker run --runtime nvidia -it --rm -p 8000:8000 slabstech/dwani-vllm
    vllm serve TinyLlama/TinyLlama-1.1B-Chat-v1.0 --host 0.0.0.0 --port 8000
    ```
- Terminal 2
    ```bash
    python api-server.py
    ```
- Terminal 3
    ```bash
    python client.py
    ```


Add - daemon.json to /etc/docker/
- sudo systemctl restart docker



 vllm serve google/gemma-3-4b-it     --served-model-name gemma3     --host 0.0.0.0     --port 8000     --gpu-memory-utilization 0.9     --tensor-parallel-size 1     --max-model-len 16384     --dtype bfloat16 


Step	Command/Notes


```bash

sudo apt-get install build-essential libnuma-dev

sudo apt remove cmake

wget https://github.com/Kitware/CMake/releases/download/v3.31.8/cmake-3.31.8-linux-aarch64.sh
chmod +x cmake-3.31.8-linux-aarch64.sh
sudo ./cmake-3.31.8-linux-aarch64.sh --prefix=/usr/local --exclude-subdir

pip uninstall torch torchvision torchaudio

pip install torch==2.7.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu128



git clone https://github.com/vllm-project/vllm.git


python use_existing_torch.py 

pip install twine setuptools-scm
pip install --upgrade setuptools

pip install -r requirements/cuda.txt
pip install -vvv -e . --no-build-isolation

VLLM_TARGET_DEVICE=gpu python setup.py bdist_wheel
pip install dist/*.whl
```


Ignoring importlib_metadata: markers 'python_version < "3.10"' don't match your environment
Ignoring six: markers 'python_version > "3.11"' don't match your environment
Ignoring setuptools: markers 'python_version > "3.11"' don't match your environment
Ignoring numba: markers 'python_version == "3.9"' don't match your environment
Ignoring xformers: markers 'platform_system == "Linux" and platform_machine == "x86_64"' don't match your 


---

docker run --gpus all -it --rm --ipc=host nvcr.io/nvidia/pytorch:23.10-py3

# Inside the container
$ pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128 # Currently, only the PyTorch nightly has wheels for aarch64 with CUDA.
$ git clone https://github.com/vllm-project/vllm.git
$ cd vllm
$ python use_existing_torch.py # remove all vllm dependency specification of pytorch
$ pip install -r requirements-build.txt # install the rest build time dependency
$ pip install -vvv -e . --no-build-isolation # use --no-build-isolation to build with the current pytorch

# Install Triton otherwise throws Triton Module Not Found
$ git clone https://github.com/triton-lang/triton.git
$ cd triton
$ pip install ninja cmake wheel pybind11 # build-time dependencies
$ pip install -e python



pip uninstall torch torchvision torchaudio

pip install torch==2.7.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu128


python use_existing_torch.py 

pip install -vvv -e . --no-build-isolation



- pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128

https://github.com/vllm-project/vllm/issues/10459

python use_existing_torch.py 


-- cmake error

sudo apt remove cmake

wget https://github.com/Kitware/CMake/releases/download/v3.31.8/cmake-3.31.8-linux-aarch64.sh
chmod +x cmake-3.31.8-linux-aarch64.sh
sudo ./cmake-3.31.8-linux-aarch64.sh --prefix=/usr/local --exclude-subdir

cmake --version

