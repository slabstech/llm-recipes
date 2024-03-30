# Install Everything for llm-recpies from scratch

- Ubuntu Library setup
    - After Ubuntu is installed, update all required libraries
        - sudo apt-get update
        - sudo apt-get upgrade
        - sudo apt dist-upgrade
        - sudo apt upgrade
        - sudo apt install git
    - Download VScode from [link](https://code.visualstudio.com/docs/?dv=linux64_deb)
        - cd Downloads && sudo dpkg -i code_*.deb
    - Install Docker  - [Install](https://docs.docker.com/engine/install/ubuntu/) & [Post-install](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user) 
        - sudo apt-get update
        - sudo apt-get install ca-certificates curl
        - sudo install -m 0755 -d /etc/apt/keyrings
        - sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
        - sudo chmod a+r /etc/apt/keyrings/docker.asc
        - ` echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \ `
        - sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        - sudo apt-get update
        - sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        - sudo docker run hello-world
        - sudo groupadd docker
        - sudo usermod -aG docker $USER
        - newgrp docker
        - docker run hello-world
    - Docker Desktop - [Optional](https://docs.docker.com/desktop/install/ubuntu/)
        - sudo apt install gnome-terminal
        - Download the deb package
        - cd Downloads && sudo dpkg -i docker-desktop*.deb
        - sudo apt-get install -f
    - Setup ssh authentication to GitHub [Step 1](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) & [Step 2](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) 


- NVIDIA - Driver setup
    - nvidia container toolkit (install)[https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html]
        - `curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
    && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list`
        - sudo apt-get update
        - sudo apt-get install -y nvidia-container-toolkit
    - Configure docker
        - sudo nvidia-ctk runtime configure --runtime=docker
        - systemctl --user restart docker
        - sudo nvidia-ctk config --set nvidia-container-cli.no-cgroups --in-place
    - Install [cuda][https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#prepare-ubuntu] & [cuda-driver](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/) & [downloads](wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin) . Note - Below versions are applicable as of March 30, 2024. You will have different version later. This is only a guide of steps.
        - sudo apt install build-essential
        - wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
        - sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
        - wget https://developer.download.nvidia.com/compute/cuda/12.4.0/local_installers/cuda-repo-ubuntu2204-12-4-local_12.4.0-550.54.14-1_amd64.deb
        - sudo dpkg -i cuda-repo-ubuntu2204-12-4-local_12.4.0-550.54.14-1_amd64.deb
        - sudo cp /var/cuda-repo-ubuntu2204-12-4-local/cuda-*-keyring.gpg /usr/share/keyrings/
        - sudo apt-get update
        - sudo apt-get -y install cuda-toolkit-12-4
        - sudo apt-get install cuda-toolkit
        - sudo reboot

- llm-recipes library
    - git clone https://github.com/slabstech/llm-recipes
