Gh200 - setup


- llama.cpp
- https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md


```bash
sudo apt-get install ninja-build

sudo apt-get install libcurl4-openssl-dev


git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp

cmake -B build -DGGML_CUDA=ON

cmake --build build --config Release
```

https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-gguf/blob/main/gemma-3-12b-it-q4_0.gguf


https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-gguf/blob/main/mmproj-model-f16-12B.gguf

- https://huggingface.co/collections/google/gemma-3-qat-67ee61ccacbf2be4195c265b

```bash
wget --header="Authorization: Bearer $HF_TOKEN" \
"https://huggingface.co/unsloth/gemma-3-12b-it-GGUF/resolve/main/gemma-3-12b-it-Q8_0.gguf" \
-O gemma-3-12b-it-Q8_0.gguf


wget --header="Authorization: Bearer $HF_TOKEN" \
"https://huggingface.co/unsloth/gemma-3-12b-it-GGUF/resolve/main/mmproj-BF16.gguf" \
-O mmproj-BF16.gguf
```

```bash
./build/bin/llama-server \
  --model gemma-3-12b-it-Q8_0.gguf \
  --mmproj mmproj-BF16.gguf \
  --host 0.0.0.0 \
  --port 7860 \
  --n-gpu-layers 100 \
  --threads 1 \
  --ctx-size 8192 \
  --batch-size 512

```

 - ./build/bin/llama-server --model gemma-3-12b-it-Q8_0.gguf --mmproj mmproj-BF16.gguf --host 0.0.0.0 --port 7860
- 
./build/bin/llama-server \
  --model gemma-3-12b-it-Q8_0.gguf \
  --mmproj mmproj-BF16.gguf \
  --host 0.0.0.0 \
  --port 7860 \
  --n-gpu-layers 100 \
  --threads 1 \
  --ctx-size 8192 \
  --batch-size 512 \
  --no-mmap \
  --temp 0.7 \
  --repeat-penalty 1.1


curl -X POST http://localhost:7860/v1/chat/completions\
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-3-12b-it",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "max_tokens": 100,
    "temperature": 0.7
  }'

curl -X POST https://abcd.hf.space/v1/chat/completions\
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-3-12b-it",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "max_tokens": 100,
    "temperature": 0.7
  }'


python -m venv --system-site-packages venv


<!-- 
pip install transformers diffusers["torch"] tf-keras==2.17.0 accelerate

pip install vllm

pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124


git clone https://github.com/vllm-project/vllm.git
cd vllm


python use_existing_torch.py


pip install -r requirements/build.txt


pip install --no-build-isolation -e .

-->
---

- https://docs.lambda.ai/education/running-huggingface-diffusers-transformers-gh200/

- https://lambda.ai/blog/putting-the-nvidia-gh200-grace-hopper-superchip-to-good-use-superior-inference-performance-and-economics

- https://docs.lambda.ai/education/fine-tune-mochi-gh200/

- https://docs.lambda.ai/public-cloud/on-demand/troubleshooting/#why-lambdas-gh200-specifications-differ-from-nvidias
