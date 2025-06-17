openai - API


- Setup Project
    ```bash
    python3.10 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
- Terminal 1
    ```bash
    export CUDA_VISIBLE_DEVICES=""
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