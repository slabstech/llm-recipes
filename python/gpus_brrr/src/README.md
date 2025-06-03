GPUs Brrr

- Setup llama.cpp to run Qwen3-0.6B
  - git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp

cmake -B build -DGGML_CUDA=ON

cmake --build build --config Release -j2


python -m venv --system-site-packages venv
source venv/bin/activate
pip install huggingface_hub
mkdir hf_models 
huggingface-cli download google/gemma-3-27b-it-qat-q4_0-gguf --local-dir hf_models/

- https://github.com/yachty66/gpu-benchmark/blob/main/src/gpu_benchmark/benchmarks/qwen3_0_6b.py