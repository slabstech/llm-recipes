Server Optimisation

- System Specification - 
  - 64 vCPUs
  - 432 GB RAM
  - 96 GB VRAM
  - 4 TB SSD

- Features
  - ASR
  - TTS
  - Translate
  - LLM   - Gemma3-27B-IT-QAT, Qwen3-30-A3, Sarvam-M
    - Chat
    - Vision
    - Docs
    - Tool Call

```python
pip install hf_xet
```

- LLM Models Setup
  - gemma3
    - huggingface-cli download google/gemma-3-27b-it-qat-q4_0-gguf --local-dir hf_models/
  - qwen3 - https://huggingface.co/Qwen/Qwen3-30B-A3B-GGUF
    - huggingface-cli download Qwen/Qwen3-30B-A3B-GGUF --include Qwen3-30B-A3B-Q8_0.gguf --local-dir hf_models/
    - ./llama-cli -hf Qwen/Qwen3-30B-A3B:Q8_0 --jinja --color -ngl 99 -fa -sm row --temp 0.6 --top-k 20 --top-p 0.95 --min-p 0 --presence-penalty 1.5 -c 40960 -n 32768 --no-context-shift
    - ./llama-server --model hf_models/Qwen3-30B-A3B-Q8_0.gguf --ngl 99 --flash-attn --context-size 40960
    - ./build/bin/llama-server \
  --model hf_models/Qwen3-30B-A3B-Q8_0.gguf \
  --host 0.0.0.0 \
  --port 7880 \
  --n-gpu-layers 100 \
  --threads 1 \
  --ctx-size 8192 \
  --batch-size 512
    - curl http://localhost:7880/completion \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a poem about AI.",
    "temperature": 0.6,
    "top_k": 20,
    "top_p": 0.95,
    "min_p": 0,
    "presence_penalty": 1.5,
    "n_predict": 32768,
    "sampler": "row",
    "use_jinja": true,
    "no_context_shift": true,
    "stream": false
  }'



  - sarvam-m
