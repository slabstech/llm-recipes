
v1 = Build a ChatGPT like setup on local machine
with Ollama + Open-WebUI + Mistral + Docker

- Requirements
    - CUDA installation - Needs NVIDIA Graphics Card
    - Docker Setup / Docker Desktop on Windows
    - VSCode Terminal

- Steps - (VSCode Terminal)
    - Clone Repo - https://github.com/slabstech/llm-recipes
        - `git clone https://github.com/slabstech/llm-recipes.git`
        - `cd llm-recipes`
    - From src/ollama directory, run the command
        - `cd src/ollama`
        - `docker-compose.exe -f .\docker-compose.yml up -d`
        - Verify if ollama backend is running at http://localhost:11434
    - Sign Up with any credentials at http://localhost:3000/auth/
    - 

    - To make UI accessible across local network
        - Windows
            - Enable Network Sharing
            - Create Firewall rule with command on Windows PowerShell
                - `New-NetFirewallRule -DisplayName "UI for LLM" -Direction Inbound -Protocol TCP -LocalPort 3000 -Action Allow`
            - Get IP address from CMD shell
                - `ipconfig`
                - Check for IPv4 Address for WIFI/LAN(Ethernet Adaptor)
            - Access from Mobile/Laptop Brower fron the local network
                - < YourIPAddress >:3000


- References
    - Download models and UI 
        - https://www.youtube.com/watch?v=syR0fT0rkgY&t=314s
    - https://medium.com/@omargohan/using-ollama-in-your-ide-with-continue-e8cefeeee033
    - https://github.com/open-webui/open-webui
    - https://github.com/ollama
    - mistral.ai

TODO - 

- Tutorial- LLM RECIPES 

Provide link for Docker and Cuda installation. 

Update steps for linux / GPU server 

- open step
- how to build hardware and system build 

Function calling and RAG with RLHF