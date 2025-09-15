sarvam Translate

- https://huggingface.co/sarvamai/sarvam-translate

- Server 
  - GGUF's
    - https://huggingface.co/mradermacher/sarvam-translate-GGUF/
    - Run with llama.cpp 
        - git clone --depth 1 https://github.com/ggml-org/llama.cpp.git
cd llama.cpp

cmake -B build -DGGML_CUDA=ON

cmake --build build --config Release -j2

python3 -m venv venv
source venv/bin/activate
pip install huggingface_hub
mkdir hf_models

huggingface-cli download mradermacher/sarvam-translate-GGUF sarvam-translate.mmproj-Q8_0.gguf --local-dir hf_models/ --local-dir-use-symlinks False

huggingface-cli download mradermacher/sarvam-translate-GGUF sarvam-translate.Q8_0.gguf --local-dir hf_models/ --local-dir-use-symlinks False

 


        - ./build/bin/llama-server -hf mradermacher/sarvam-translate-GGUF:Q4_K_M --host 0.0.0.0 --port 8000 --n-gpu-layers 99 --ctx-size 1008 --alias gemma3 
  - vLLM
    - vllm serve sarvamai/sarvam-translate --port 8000 --dtype bfloat16 --max-model-len 8192

- Client
  - python client.py


- Note : 
    - choose the quantization based on VRAM
    - https://huggingface.co/mradermacher/sarvam-translate-GGUF

- For Multimodal
    - 