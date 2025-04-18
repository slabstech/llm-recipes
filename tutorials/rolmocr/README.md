RolmOCR

sudo apt-get update

sudo apt-get install poppler-utils ttf-mscorefonts-installer msttcorefonts fonts-crosextra-caladea fonts-crosextra-carlito gsfonts lcdf-typetools


-- USe arrow button - to accept the license
git clone --depth 1 https://github.com/allenai/olmocr.git



cd olmocr

python3.10 -m venv venv

source venv/bin/activate

- change pyproject.toml - set python to 3.10




pip install --upgrade pip

pip install uv

uv pip install "sglang[all]" --find-links https://flashinfer.ai/whl/cu124/torch2.6/flashinfer-python

pip install -r requirements.txt

pip install -e .


uvicorn olmo_api_v2:app --host 0.0.0.0 --port 7860

----



// python -m olmocr.pipeline ./localworkspace --pdfs tests/gnarly_pdfs/horribleocr.pdf

wget https://slabstech.com/assets/pdf/alemaari.pdf

cp alemaari.pdf paper.pdf 



----




 curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path --profile minimal

  export PATH="/root/.cargo/bin:${PATH}"

  export CC=/usr/bin/gcc

  export ENV CXX=/usr/bin/g++

  pip install --no-cache-dir --upgrade pip setuptools psutil setuptools-rust torch


export ENV CXX=/usr/bin/g++
https://huggingface.co/reducto/RolmOCR

mkdir rolmocr
cd rolmocr/

python3.10 -m venv venv

source venv/bin/activate


pip install vllm

pip install -U "huggingface_hub[cli]"

huggingface-cli download  reducto/RolmOCR-7b

export VLLM_USE_V1=1
vllm serve reducto/RolmOCR --host 0.0.0.0 --port 8000

pip install fastapi uvicorn openai python-multipart


pip install olmocr

