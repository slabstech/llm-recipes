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

sudo apt update


sudo apt install -y docker.io

sudo systemctl status docker


docker --version

sudo usermod -aG docker $USER


