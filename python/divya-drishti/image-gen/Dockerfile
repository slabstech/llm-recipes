FROM nvidia/cuda:12.8.0-cudnn-devel-ubuntu22.04
WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip python3-distutils python3-dev python3-venv\
    git \
    ffmpeg \
    sudo wget curl software-properties-common build-essential gcc g++ \   
    && ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN export CC=/usr/bin/gcc
RUN export CXX=/usr/bin/g++

RUN pip install --upgrade pip setuptools setuptools-rust torch
RUN pip install flash-attn --no-build-isolation

COPY requirements.txt .
#RUN pip install --no-cache-dir torch==2.6.0 torchvision
#RUN pip install --no-cache-dir transformers
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install git+https://github.com/ai4bharat/IndicF5.git

COPY . .

RUN useradd -ms /bin/bash appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 7860

# Run the server
CMD ["python", "/app/ghost_vision.py"]