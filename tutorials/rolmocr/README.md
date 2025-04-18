PDF - Extractor

Setup 

sudo apt-get update

sudo apt-get install poppler-utils ttf-mscorefonts-installer msttcorefonts fonts-crosextra-caladea fonts-crosextra-carlito gsfonts lcdf-typetools


- RolmOCR

python3.10 -m venv venv

source venv/bin/activate

pip install rolmo_requirements.txt
export VLLM_USE_V1=1
vllm serve reducto/RolmOCR 

python rolmo/api.py



For OlMOCR 


sudo apt-get update

sudo apt-get install poppler-utils ttf-mscorefonts-installer msttcorefonts fonts-crosextra-caladea fonts-crosextra-carlito gsfonts lcdf-typetools

-- USe arrow button - to accept the license

python3.10 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install uv

uv pip install "sglang[all]" --find-links https://flashinfer.ai/whl/cu124/torch2.6/flashinfer-python

pip install -r requirements.txt

pip install git+https://github.com/slabstech/olmocr.git@dhwani-docs




uvicorn olmo_api_v2:app --host 0.0.0.0 --port 7860

----