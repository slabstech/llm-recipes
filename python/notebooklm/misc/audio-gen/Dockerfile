FROM nvidia/cuda:12.2.0-base-ubuntu22.04

RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip 

RUN git clone https://github.com/Stability-AI/stable-audio-tools.git
WORKDIR /stable-audio-tools


RUN pip3 install .

# Download model weights
RUN mkdir checkpoints && \
    wget -O checkpoints/stable-audio-1_0-base.pth https://huggingface.co/stabilityai/stable-audio-1.0-base/resolve/main/stable-audio-1_0-base.pth

COPY generate_audio.py .

CMD ["python3", "generate_audio.py"]
