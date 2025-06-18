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
Install Tools - 	sudo apt-get install build-essential cmake libnuma-dev
Clone - 	git clone https://github.com/vllm-project/vllm.git
Requirements -	pip install -r requirements-build.txt
pip install -r requirements-gpu.txt
Build Wheel	- VLLM_TARGET_DEVICE=gpu python setup.py bdist_wheel
Install	pip install dist/*.whl

