Open WebUI


sudo docker compose -f open-webui-compose.yml up -d

alternate command

```bash
docker run -d -p 21000:21000 -e PORT=21000 --name open-webui ghcr.io/open-webui/open-webui:main

docker run -d -p 21000:21000 -e PORT=21000 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
```

Source - https://github.com/open-webui/open-webui

Web - https://openwebui.com/

--

docker pull --platform linux/amd64 ghcr.io/open-webui/open-webui:main


gcloud auth configure-docker us-central1-docker.pkg.dev


docker tag ghcr.io/open-webui/open-webui:main us-central1-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/openwebui
docker push us-central1-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/openwebui


--
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list


curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -





sudo apt-get update
sudo apt-get install google-cloud-cli


--

Setup google VM





---

For Debian

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo systemctl status docker


docker --version

sudo usermod -aG docker $USER


---

api -server
sudo apt update
sudo apt upgrade -y
sudo apt install git python3.11-venv


git clone https://huggingface.co/spaces/dwani/dwani-api

cd dwani-api

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


sudo apt install python3-pip
sudo pip install -r requirements.txt

sudo pip install --break-system-packages -r requirements.txt

 sudo python3 src/server/main.py --host 0.0.0.0 --port 80

 