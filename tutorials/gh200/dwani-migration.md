dwani.ai - gh200


ASR - https://github.com/dwani-ai/asr-indic-server.git

TTS - https://github.com/dwani-ai/tts-indic-server.git

Docs - https://github.com/dwani-ai/docs-indic-server.git

Translate

LLM

dwani-server 


To use pytorch on 
python -m venv --system-site-packages venv


https://huggingface.co/spaces/dwani/gh-200-indic-translate-server 

https://huggingface.co/spaces/dwani/gh-200-docs-indic-server 

curl -X POST http://lambda-sip:7860/v1/chat/completions -H "Content-Type: application/json" -d '{
  "model": "gemma-3-12b-it-Q8_0.gguf",
  "messages": [
    {"role": "user", "content": "Hello, who are you?"}
  ]
}'


---

sudo apt install poppler-utils


sudo apt-get install -y build-essential python3-dev python3-setuptools make cmake
sudo apt-get install -y ffmpeg libavcodec-dev libavfilter-dev libavformat-dev libavutil-dev

git clone --recursive https://github.com/dmlc/decord

cd decord

mkdir build && cd build

cmake .. -DUSE_CUDA=0 -DCMAKE_BUILD_TYPE=Release

make

cd ../python

pwd=$PWD
echo "PYTHONPATH=$PYTHONPATH:$pwd" >> ~/.bashrc
source ~/.bashrc
# option 2: install with setuptools
python3 setup.py install --user



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
-requires-python = ">=3.11"
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