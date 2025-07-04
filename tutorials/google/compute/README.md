Google - VM Setup

sudo apt install nano git -y

sudo    apt install python3.12-venv -y

 git clone https://github.com/dwani-ai/dwani-api-server.git

 cd dwani-api-server
 python3 -m venv venv
 source venv/bin/activate
pip install --upgrade pip
pip install setuptools-rust

 pip install -r requirements.txt

sudo python src/server/main.py --host  0.0.0.0 --port 80


export API_KEY_SECRET="dwani-moasdsbile-app"
export CHAT_RATE_LIMIT="100/minute"
export DWANI_API_BASE_URL_PDF="http://127.0.0.1:7861"
export DWANI_API_BASE_URL_VISION="http://127.0.0.1:7861"
export DWANI_API_BASE_URL_LLM="http://127.0.0.1:7861"
export DWANI_API_BASE_URL_LLM_QWEN="http://127.0.0.1:7880"
export DWANI_API_BASE_URL_TTS="http://127.0.0.1:7864"
export DWANI_API_BASE_URL_ASR="http://127.0.0.1:7863"
export DWANI_API_BASE_URL_TRANSLATE="http://127.0.0.1:7862"
export DWANI_API_BASE_URL_S2S="http://127.0.0.1:7861"
export SPEECH_RATE_LIMIT="5/minute"
export ENCRYPTION_KEY="tetasdasde"
export DEFAULT_ADMIN_USER="admiasdasdan"
export DEFAULT_ADMIN_PASSWORD="dwani-987-123asdasd"