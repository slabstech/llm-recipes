Google - VM Setup

sudo yum install git -y


 git clone https://github.com/dwani-ai/dwani-api-server.git

 cd dwani-api-server
 python3 -m venv venv
 source venv/bin/activate

 pip install -r requirements.txt