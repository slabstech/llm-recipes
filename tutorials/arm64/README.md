vLLM for arm64 

- For GH200, GB200 Nvidia GPU

- Python - vllm arm64 wheel on GitHub 
  - https://github.com/dwani-ai/vllm-arm64/releases/download/v0.0.1/vllm-0.9.2.dev144+g9206d0ff0.d20250618-cp310-cp310-linux_aarch64.whl


- vllm arm64 docker container 
 - https://hub.docker.com/r/dwani/vllm-arm64 
 - docker pull dwani/vllm-arm64:latest
 

- Create vllm library 
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



<!-- 
Add - daemon.json to /etc/docker/
- sudo systemctl restart docker
--> 



