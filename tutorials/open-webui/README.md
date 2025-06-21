Open WebUI


sudo docker compose -f open-webui-compose.yml up -d

alternate command

```bash
docker run -d -p 21000:21000 -e PORT=21000 --name open-webui ghcr.io/open-webui/open-webui:main

docker run -d -p 21000:21000 -e PORT=21000 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
```

Source - https://github.com/open-webui/open-webui

Web - https://openwebui.com/

