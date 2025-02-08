FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime
# hadolint ignore=DL3008,DL3015,DL4006
RUN apt-get update && \
    apt-get install -y git curl software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3.12 python3.12-distutils && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root/magnet-server

# Install audiocraft/magnet from GitHub
RUN pip3.12 install --no-cache-dir --no-deps git+https://github.com/audiocraft/magnet.git

# Copy and install additional requirements
COPY ./model_requirements.txt .
RUN pip3.12 install --no-cache-dir -r model_requirements.txt

COPY ./server_requirements.txt .
RUN pip3.12 install --no-cache-dir -r server_requirements.txt

# Copy the server code
COPY ./magnet_server ./magnet_server

CMD ["uvicorn", "magnet_server.main:app"]
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8000