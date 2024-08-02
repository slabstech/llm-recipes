Segment Anythinh2



- Source
  - 
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

- Fresh CUDA - Re Install
  - sudo apt-get remove --purge '^cuda-.*'
  - sudo apt-get remove --purge '^libnvidia-.*'
  - sudo apt-get remove --purge '^cuda-.*'
