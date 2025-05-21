dwani.ai - gh200


export API_KEY_SECRET="dwani-mobile-app-some-sercwer234"
export CHAT_RATE_LIMIT="100/minute"
export DWANI_API_BASE_URL_PDF="http://127.0.0.1:7861"
export DWANI_API_BASE_URL_VISION="http://127.0.0.1:7861"
export DWANI_API_BASE_URL_LLM="http://127.0.0.1:7861"
export DWANI_API_BASE_URL_TTS="http://127.0.0.1:7860"
export DWANI_API_BASE_URL_ASR="http://127.0.0.1:7863"
export DWANI_API_BASE_URL_TRANSLATE="http://127.0.0.1:7862"
export DWANI_API_BASE_URL_S2S="http://127.0.0.1:7861"
export SPEECH_RATE_LIMIT="5/minute"
export ENCRYPTION_KEY="tetegdgfdgfdfgdfgdfg"
export DEFAULT_ADMIN_USER="adminsdfsdf"
export DEFAULT_ADMIN_PASSWORD="dwani-987-123234fsfsfsfsfd"

export HF_TOKEN='hf_this_is_not_a_secret__this_gaganyatri'

- Router

git clone https://github.com/dwani-ai/dwani-api-server
cd dwani-api-server

python -m venv --system-site-packages venv

source venv/bin/activate

pip install -r requirements.txt


python src/server/main.py --host  0.0.0.0 --port 8888



- ASR 
    - https://github.com/dwani-ai/asr-indic-server.git
    - git clone https://huggingface.co/spaces/dwani/gh200-asr-indic-server
    python -m venv --system-site-packages venv

source venv/bin/activate

pip install -r requirements.txt

    python src/server/asr_api.py --host 0.0.0.0 --port 7863 --device cuda


-  Docs 
  - https://github.com/dwani-ai/docs-indic-server.git
  - git clone https://huggingface.co/spaces/dwani/gh-200-docs-indic-server
python -m venv --system-site-packages venv

source venv/bin/activate

pip install -r requirements.txt

- Translate
  - git clone https://huggingface.co/spaces/dwani/gh-200-indic-translate-server
  python -m venv --system-site-packages venv

source venv/bin/activate

pip install -r requirements.txt
  pip install "numpy<2.0"
python src/server/translate_api.py --host 0.0.0.0 --port 7862 --device cuda



- 
TTS - https://github.com/dwani-ai/tts-indic-server-f5


To use pytorch on GH 200 
python -m venv --system-site-packages venv


curl -X POST http://lambda-sip:7860/v1/chat/completions -H "Content-Type: application/json" -d '{
  "model": "gemma-3-12b-it-Q8_0.gguf",
  "messages": [
    {"role": "user", "content": "Hello, who are you?"}
  ]
}'


---
for docs-indic-server

sudo apt install -y poppler-utils


sudo apt-get install -y build-essential python3-dev python3-setuptools make cmake
sudo apt-get install -y ffmpeg libavcodec-dev libavfilter-dev libavformat-dev libavutil-dev

git clone --recursive https://github.com/dmlc/decord

cd decord

mkdir build && cd build

cmake .. -DUSE_CUDA=0 -DCMAKE_BUILD_TYPE=Release

make

cd ../python


// pwd=$PWD
// echo "PYTHONPATH=$PYTHONPATH:$pwd" >> ~/.bashrc
// source ~/.bashrc
# option 2: install with setuptools
python3 setup.py install --user



pip install "numpy<2.0"


-
git clone  https://github.com/allenai/olmocr.git

cd olmocr
pip install --upgrade pip setuptools wheel packaging
pip install -e .
pip install "numpy<2.0"

in olmocr :  pyproject.toml - remove sql-kernem and sglang
set python version to 3.10
<!--

diff --git a/pyproject.toml b/pyproject.toml
index 0eec834..431216f 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -17,7 +17,7 @@ classifiers = [
 authors = [
     {name = "Allen Institute for Artificial Intelligence", email = "jakep@allenai.org"}
 ]
-requires-python = ">=3.11"git 
+requires-python = ">=3.10"
 dependencies = [
   "cached-path",
   "smart_open",
@@ -50,8 +50,6 @@ Changelog = "https://github.com/allenai/olmocr/blob/main/CHANGELOG.md"
 
 [project.optional-dependencies]
 gpu = [
-    "sgl-kernel==0.0.3.post1",
-    "sglang[all]==0.4.2",
 ]
 
 dev = [
 -->

 --


 git clone https://github.com/dwani-ai/dwani-api-server.git

python -m venv --system-site-packages venv
source venv/bin/activate
python src/server/main.py --host 0.0.0.0 --port 78878