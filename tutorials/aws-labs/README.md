AWS setup



sudo apt install python3.10-venv



sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    git \
    ffmpeg \
    curl \
    build-essential


git clone https://huggingface.co/spaces/slabstech/dhwani-server-workshop

cd dhwani-server-workshop
python3.10 -m venv venv


 source venv/bin/activate


  export EXTERNAL_API_BASE_URL=http://example.com

-- Run server in backgorund
   python src/server/main.py --host 0.0.0.0 --port 7860  &


--
Pending - Enable - https
https://www.perplexity.ai/search/enable-https-for-ec2-instance-5T_9aMGfRT.vBoyI45oBSg
