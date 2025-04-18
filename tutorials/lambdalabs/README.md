Lambda labs

- Use Cloude IDE / Jupyter Labs

https://huggingface.co/spaces/slabstech/dhwani-internal-api-server


- Setup - Dhwani Model Server

git clone https://huggingface.co/spaces/slabstech/dhwani-internal-api-server


sudo apt-get install ffmpeg build-essential

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path --profile minimal 

export PATH="/root/.cargo/bin:${PATH}"
export CC=/usr/bin/gcc
export ENV CXX=/usr/bin/g++

python3.10 -m venv venv

source venv/bin/activate

pip install --no-cache-dir --upgrade pip setuptools psutil setuptools-rust torch
pip install --no-cache-dir flash-attn  --no-build-isolation 

pip install --no-cache-dir -r requirements.txt

export HF_HOME=/home/ubuntu/dhwani-ai-v0-0-2

export HF_TOKEN=asdasdadasd

python src/server/main.py --host 0.0.0.0 --port 7860 --config config_two


-- 

Update Firewall Rules

- Add Custom TCP - Set port to 7860 . 

Use http://IP-ADDress:7860/docs to access dhwani-server

