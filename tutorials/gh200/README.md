Gh200

https://docs.lambda.ai/education/running-huggingface-diffusers-transformers-gh200/

https://lambda.ai/blog/putting-the-nvidia-gh200-grace-hopper-superchip-to-good-use-superior-inference-performance-and-economics

https://docs.lambda.ai/education/fine-tune-mochi-gh200/

https://docs.lambda.ai/public-cloud/on-demand/troubleshooting/#why-lambdas-gh200-specifications-differ-from-nvidias


llama.cpp


https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md



sudo apt-get install ninja-build

sudo apt-get install libcurl4-openssl-dev


git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp

cmake -B build -DGGML_CUDA=ON

cmake --build build --config Release


https://huggingface.co/collections/google/gemma-3-qat-67ee61ccacbf2be4195c265b


wget --header="Authorization: Bearer $HF_TOKEN" \
"https://huggingface.co/unsloth/gemma-3-12b-it-GGUF/resolve/main/gemma-3-12b-it-Q8_0.gguf" \
-O gemma-3-12b-it-Q8_0.gguf


wget --header="Authorization: Bearer $HF_TOKEN" \
"https://huggingface.co/unsloth/gemma-3-12b-it-GGUF/resolve/main/mmproj-BF16.gguf" \
-O mmproj-BF16.gguf




./build/bin/llama-gemma3-cli \
  --model /path/to/gemma-3-12b.q8_0.gguf \
  --mm_proj /path/to/mmproj.gguf


python -m venv --system-site-packages hf-tests



pip install transformers diffusers["torch"] tf-keras==2.17.0 accelerate

pip install vllm

pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124


git clone https://github.com/vllm-project/vllm.git
cd vllm


python use_existing_torch.py


pip install -r requirements/build.txt


pip install --no-build-isolation -e .

---
