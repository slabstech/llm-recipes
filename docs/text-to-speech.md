Text to Speech

- - Clone Repo
  - git clone https://github.com/coqui-ai/TTS.git
- Setup virtual environment
  - python -m venv venv
  - source venv/bin/activate
- Install TTS library
    - pip install TTS


- Run TTS on Terminal
  - tts --text "Text for TTS" --out_path speech.wav
  -  tts --text "My name is sachin shetty" --out_path speech.wav


- Docker Setup

- Reference
    - https://github.com/coqui-ai/TTS


version: '3'
services:
  tts:
    image: coqui/tts:latest
    volumes:
      - ./data:/root/.local/share/tts
    command: tts-server --model_name tts_models/en/vctk/vits


On host  machine ‐ 

mkdir -p data/tts_models/en/vctk/vits
wget -P data/tts_models/en/vctk/vits https://github.com/coqui-ai/TTS/releases/download/v0.11.0/vctk-vits.zip
unzip data/tts_models/en/vctk/vits/vctk-vits.zip -d data/tts_models/en/vctk/vits


https://www.perplexity.ai/search/Coqui-ai-tts-6DlPHfrkSHmq9QB3fE_cSg

Building dockerfile 

FROM nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install coqui-tts

WORKDIR /app

ENTRYPOINT ["tts-server"]
CMD ["--list_models"]

---

docker build -t coqui-tts .
-- 
docker run --rm -it -p 5002:5002 coqui-tts --model_name tts_models/en/vctk/vits
---



--
With custom model - prebuilt 

FROM nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install coqui-tts

# Download and extract the desired model(s)
RUN mkdir -p /root/.local/share/tts/tts_models/en/vctk/vits && \
    wget -O - https://github.com/coqui-ai/TTS/releases/download/v0.11.0/vctk-vits.zip | bsdtar -xvf- -C /root/.local/share/tts/tts_models/en/vctk/vits

WORKDIR /app

ENTRYPOINT ["tts-server"]
CMD ["--model_name", "tts_models/en/vctk/vits"]


-- 


Cpu only 
--

FROM python:3.8-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install coqui-tts

WORKDIR /app

ENTRYPOINT ["tts-server"]
CMD ["--list_models"]


--
docker build -t coqui-tts-cpu .

--
docker run --rm -it -p 5002:5002 coqui-tts-cpu

-- 

To optimize the Dockerfile for better performance in Coqui TTS, you can follow these steps:

    Use a smaller base image

Instead of using the larger ubuntu:20.04 base image, consider using a more lightweight base image like python:3.8-slim or nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04. This can significantly reduce the overall image size.

    Combine RUN commands

Combine multiple RUN commands into a single RUN command using && to chain them together. This reduces the number of layers in the image, making it more efficient.

dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        python3 \
        python3-pip \
        && \
    rm -rf /var/lib/apt/lists/*

    Use multi-stage builds

Implement a multi-stage build to separate the build environment from the final runtime environment. This way, you can keep the final image lean by copying only the necessary files from the build stage.

    Install dependencies from requirements file

Instead of installing coqui-tts directly, create a requirements.txt file with the required dependencies and install them using pip install -r requirements.txt. This allows better caching and faster builds when dependencies haven't changed.

    Use Docker's built-in caching mechanism

Order the instructions in your Dockerfile such that the least frequently changing instructions are at the top. This way, Docker can reuse cached layers when possible, reducing build times.

    Use NVIDIA's optimized Docker images

If you're running Coqui TTS on an NVIDIA GPU, use NVIDIA's optimized Docker images for machine learning, as they are designed for efficient model training and inference.

    Leverage Docker volumes for data persistence

Instead of copying data into the Docker image, use Docker volumes to mount the necessary data (e.g., models, datasets) from the host machine. This keeps the image size small and allows for easy data management
. By following these optimization techniques, you can significantly reduce the size of your Coqui TTS Docker image and improve its performance, making it more efficient for model training and inference.


--

Whisper with data

version: '3'
services:
  whisper:
    image: rhasspy/wyoming-whisper
    command: --model base-int8 --language en
    volumes:
      - /path/to/host/model/data:/data
    ports:
      - 10300:10300

