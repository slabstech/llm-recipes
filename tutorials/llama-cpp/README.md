llama.cpp

- Build 
  - git clone https://github.com/ggerganov/llama.cpp
  - cd llama.cpp
  - With CUDA
    - make GGML_CUDA=1

- Conver from tensor/transformer to gguf
  - python3.10 -m venv venv
  - source venv/bin/activate
  - Download the required model to models directory
    - mkdir models/sarvam
    -  huggingface-cli download sarvamai/sarvam-2b-v0.5 --local-dir models/sarvam/
  - python3 -m pip install -r requirements.txt

  - convert the model to ggml FP16 format
  - python3 convert_hf_to_gguf.py models/sarvam/
  - ./llama-quantize ./models/sarvam/sarvam-2B-v0.5-F16.gguf ./models/sarvam/sarvam-2B-v0.5-Q4_K_M.gguf Q4_K_M


  - Run the quantised model
    - ./llama-cli -m ./models/sarvam/sarvam-2B-v0.5-Q4_K_M.gguf -n 128



- Prequisites
    - nvidia-container-toolkit
    - Add to .bashrc after install
      export CUDA_HOME=/usr/local/cuda-12.6
      export PATH=$PATH:$CUDA_HOME/bin


Reference
    - https://github.com/ggerganov/llama.cpp/blob/master/docs/build.md
    - https://developer.nvidia.com/cuda-downloads
    - https://github.com/ggerganov/llama.cpp/blob/master/examples/quantize/README.md