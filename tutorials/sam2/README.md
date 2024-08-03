Segment Anythinh2



wget https://github.com/slabstech/llm-recipes/raw/ondevice-inference/tutorials/sam2/sam2-automatic.ipynb
- Source - https://github.com/facebookresearch/segment-anything-2
  - git clone https://github.com/facebookresearch/segment-anything-2.git
  - cd segment-anything-2
  - python3.10 -m venv venv
  - source venv/bin/activate
  - pip install -e .
  - python setup.py build_ext --inplace
  - pip install supervision

Download the weights
- wget -q https://dl.fbaipublicfiles.com/segment_anything_2/072824/sam2_hiera_tiny.pt

- pip install notebook

- Download the notebook
- wget https://colab.research.google.com/github/roboflow-ai/notebooks/blob/main/notebooks/how-to-segment-videos-with-sam-2.ipynb

- Video Segmentation
  - https://blog.roboflow.com/sam-2-video-segmentation/


- CUDA installation
  - https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#introduction
  - https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=deb_local

  - lspci | grep -i nvidia
  - uname -m && cat /etc/*release

  - gcc --version
  
  - wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
  - sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
  - wget https://developer.download.nvidia.com/compute/cuda/12.6.0/local_installers/cuda-repo-ubuntu2204-12-6-local_12.6.0-560.28.03-1_amd64.deb
  - sudo dpkg -i cuda-repo-ubuntu2204-12-6-local_12.6.0-560.28.03-1_amd64.deb
  - sudo cp /var/cuda-repo-ubuntu2204-12-6-local/cuda-*-keyring.gpg /usr/share/keyrings/
  - sudo apt-get update
  - sudo apt-get -y install cuda-toolkit-12-6 
  - sudo apt-get install -y nvidia-open

export CUDA_HOME=/usr/local/cuda-12.6
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH



- Fresh CUDA - Re Install
  - sudo apt-get remove --purge '^cuda-.*'
  - sudo apt-get remove --purge '^libnvidia-.*'
  - sudo apt-get remove --purge '^cuda-.*'


Access Jupyter notebook from remote server

- On Remote server
    - Create python  virtual environment
        - python -m venv venv
    - Enable virtual environment
        - source -m venv venv
    - Install Jupyter notebook
        - pip install notebook
    - Enable security for jupyter server
        - jupyter server password
            - Enter new password
    -  Start notebook 
        - jupyter notebook --no-browser --port=8888

- On Local Machine
    - ssh -L 8888:localhost:8888 remote-user@remote-server

    - vistit localhost:8888 on the browser


---


Sam + Florence

docker run -it -p 7860:7860 --platform=linux/amd64 --gpus all \
        registry.hf.space/skalskip-florence-sam:latest python app.py

git clone https://huggingface.co/spaces/SkalskiP/florence-sam

cd florence-sam

pip install -r local-requirements.txt

python app.py
