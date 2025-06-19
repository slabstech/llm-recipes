openai - API

https://github.com/dwani-ai/vllm-arm64

- To run a vllm server via python library
- Setup Project
    ```bash
    python3.10 -m venv venv
    source venv/bin/activate
    pip install fastapi uvicorn pydantic requests
    pip install torch==2.7.0 torchaudio==2.7.0 torchvision --index-url https://download.pytorch.org/whl/cu128
    pip install https://github.com/dwani-ai/vllm-arm64/releases/download/v0.0.1/vllm-0.9.2.dev144+g9206d0ff0.d20250618-cp310-cp310-linux_aarch64.whl
    python api-server.py
    ```

- To run a vllm server via docker container
    ```bash
    sudo docker run --runtime nvidia -it --rm -p 9000:9000 dwani/vllm-arm64:latest


vllm serve google/gemma-3-4b-it --served-model-name gemma3 google/gemma-3-4b-it --host 0.0.0.0 --port 9000 --gpu-memory-utilization 0.8

    vllm serve TinyLlama/TinyLlama-1.1B-Chat-v1.0 --host 0.0.0.0 --port 9000 --gpu-memory-utilization 0.5
    ```


- Send request to vllm server
    ```bash
    python client.py
    ```

- gemma3
```bash
curl -X POST http://localhost:9000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemma-3-4b-it",
    "messages": [
      {"role": "user", "content": "Tell me a joke about programming"}
    ]
  }'
```

--

```bash
curl -X POST http://localhost:9000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma3",
    "messages": [
      {"role": "user", "content": "Tell me a joke about programming"}
    ]
  }'
```

--


```bash
curl -X POST https://dwani- vllm. hf. space/v1/chat/completions \
  -H "Content-Type: application/json"\ 
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -d '{
    "model": "google/gemma-3-4b-it",
    "messages": [
      {"role": "user", "content": "Tell me a joke about programming"}
    ]
  }'
```

--

```bash
curl -X POST https://dwani- vllm. hf. space/v1/chat/completions \
  -H "Content-Type: application/json"\ 
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -d '{
    "model": "gemma3",
    "messages": [
      {"role": "user", "content": "Tell me a joke about programming"}
    ]
  }'
```
--


- tinyllama

```bash
curl -X POST http://localhost:9000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "messages": [
      {"role": "user", "content": "Tell me a joke about programming"}
    ]
  }'
```

```bash
curl -X POST https://dwani- vllm. hf. space/v1/chat/completions \
  -H "Content-Type: application/json"\ 
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -d '{
    "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "messages": [
      {"role": "user", "content": "Tell me a joke about programming"}
    ]
  }'
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

pip install torch==2.7.0 torchaudio==2.7.0 torchvision --index-url https://download.pytorch.org/whl/cu128



git clone https://github.com/vllm-project/vllm.git

cd vllm
python use_existing_torch.py 

pip install --upgrade setuptools twine setuptools-scm


pip install -r requirements/cuda.txt
export MAX_JOBS=4
pip install -vvv -e . --no-build-isolation

VLLM_TARGET_DEVICE=cuda python setup.py bdist_wheel
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

