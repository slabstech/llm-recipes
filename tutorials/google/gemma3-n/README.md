Gemma 3-n

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

huggingface-cli download onnx-community/gemma-3n-E2B-it-ONNX --repo-type model --local-dir gemma-3n-E2B-it-ONNX

python onnx_gemma.py

python example.py
```

<!-- 
- pip install transformers pillow torch accelerate onnxruntime torchvision librosa timm bitsandbytes onnxruntime-gpu
- python gemma_3_example.py

- python download.py
-->


- References 
    - https://www.kaggle.com/competitions/google-gemma-3n-hackathon/rules

    - https://developers.googleblog.com/en/introducing-gemma-3n-developer-guide/

    - https://ai.google.dev/gemma/docs/gemma-3n

    - Jetson
      - https://developer.nvidia.com/blog/run-google-deepminds-gemma-3n-on-nvidia-jetson-and-rtx/?ncid=so-twit-239330