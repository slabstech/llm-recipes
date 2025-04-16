Lambda labs

- Use Cloude IDE / Jupyter Labs


apt-get install ffmpeg build-essential

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path --profile minimal \
    && rm -rf /root/.rustup/toolchains/*/share/doc

ENV PATH="/root/.cargo/bin:${PATH}"
ENV CC=/usr/bin/gcc
ENV CXX=/usr/bin/g++

pip install --no-cache-dir --upgrade pip setuptools setuptools-rust torch
pip install --no-cache-dir flash-attn  --no-build-isolation 

