RolmOCR

sudo apt-get update

sudo apt-get install poppler-utils ttf-mscorefonts-installer msttcorefonts fonts-crosextra-caladea fonts-crosextra-carlito gsfonts lcdf-typetools

-- USe arrow button - to accept the license

python3.10 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install uv

uv pip install "sglang[all]" --find-links https://flashinfer.ai/whl/cu124/torch2.6/flashinfer-python

pip install -r requirements.txt


git clone --depth 1 https://github.com/allenai/olmocr.git


cd olmocr


- change pyproject.toml - set python to 3.10


pip install -e .


uvicorn olmo_api_v2:app --host 0.0.0.0 --port 7860

----