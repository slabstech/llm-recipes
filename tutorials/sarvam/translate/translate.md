sarvam Translate

- https://huggingface.co/sarvamai/sarvam-translate
    - GGUF's
        - https://huggingface.co/mradermacher/sarvam-translate-GGUF/
        - Run with llama.cpp 
            - llama-server -hf mradermacher/sarvam-translate-GGUF:Q4_K_M --host 0.0.0.0 --port 9000 --n-gpu-layers 99 --ctx-size 1008 --alias gemma3 

    - vLLM
        - vllm serve sarvamai/sarvam-translate --port 8000 --dtype bfloat16 --max-model-len 8192

- 