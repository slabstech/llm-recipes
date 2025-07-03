Google - VM Setup

sudo yum install git -y


 git clone https://github.com/dwani-ai/dwani-api-server.git

 cd dwani-api-server
 python3 -m venv venv
 source venv/bin/activate
pip install --upgrade pip
pip install setuptools-rust

 pip install -r requirements.txt

 python src/server/main.py --host  0.0.0.0 --port