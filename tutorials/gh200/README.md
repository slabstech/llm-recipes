Gh200 - setup

mkdir dwani_org
cd dwani_org
- llama.cpp
- https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md


```bash
sudo apt-get install ninja-build

sudo apt-get install libcurl4-openssl-dev

sudo apt-get install -y build-essential python3-dev python3-setuptools make cmake
sudo apt-get install -y ffmpeg libavcodec-dev libavfilter-dev libavformat-dev libavutil-dev
sudo apt install -y poppler-utils


git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp

cmake -B build -DGGML_CUDA=ON

cmake --build build --config Release -j2
```



```bash 
python -m venv --system-site-packages venv
source venv/bin/activate
pip install huggingface_hub
mkdir hf_models 
huggingface-cli download google/gemma-3-27b-it-qat-q4_0-gguf --local-dir hf_models/

 ./build/bin/llama-server   --model hf_models/gemma-3-27b-it-q4_0.gguf  --mmproj hf_models/mmproj-model-f16-27B.gguf  --host 0.0.0.0   --port 7860   --n-gpu-layers 100   --threads 1   --ctx-size 8192   --batch-size 512
```



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
