dwani.ai

- Server Setup

- System Library setup 
```bash
sudo apt-get update

sudo apt-get install -y ffmpeg build-essential
sudo apt-get install -y poppler-utils ttf-mscorefonts-installer msttcorefonts fonts-crosextra-caladea fonts-crosextra-carlito gsfonts lcdf-typetools

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path --profile minimal
```

-


docs-indic-server

python src/server/docs_api_dwani.py 

