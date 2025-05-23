API Server

Proxy Server

git clone https://github.com/dwani-ai/proxy-server.git
cd proxy-server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python src/server/main.py

Load balancer


python src/server/load_balancer.py