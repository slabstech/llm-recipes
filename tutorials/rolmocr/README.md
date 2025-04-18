RolmOCR


https://huggingface.co/reducto/RolmOCR

mkdir rolmocr
cd rolmocr/

python3.10 -m venv venv

source venv/bin/activate


pip install vllm


export VLLM_USE_V1=1
vllm serve reducto/RolmOCR --host 0.0.0.0 --port 8000

pip install fastapi uvicorn openai python-multipart