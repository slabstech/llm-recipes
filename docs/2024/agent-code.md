simulation  Agents

- Autogen 
    - https://github.com/microsoft/autogen

- Setup
    - python3 -m venv pyautogenvenv
        - Linux -  source pyautogenvenv/bin/activate
        - Windows - .\pyautogenvenv\Scripts\activate
    - pip install pyautogen
    - Docker setup - In a different directory
        - git clone --depth=1 https://github.com/microsoft/autogen
        - docker build -f .devcontainer/Dockerfile -t autogen_base_img https://github.com/microsoft/autogen.git#main
    
- Examples
    - simple-agent
    - docker-code-executor
    - multi-agent-research

- Require individual endpoints for Agents to work efficiently.
- Create ollama containers and use it with docker compose. Build with hardcoded API endpoints initially and later optimise with load-balancer.

- Use smaller models to fit into GPU memory. Example 
    - 24 GB card (RTX 4 series) can support 3 x- mistral 7B models
    - 12 GB card (RTX 3 series) can support 4 x - gemma2B model
    - 6 GB card (GTX 1060) can support 2 x - gemma2B model

- Run the different agent models in docker container
    - 



1) Use a large model (Opus/GPT-4) to break down a problem & generate prompts/variables/tasks/examples

2) Use cheap (and way faster) models like Haiku to do the actual work

KSP - 

https://wiki.kerbalspaceprogram.com/wiki/Tutorial:Understanding_Addon_Code

https://wiki.kerbalspaceprogram.com/wiki/API:Part

https://github.com/topics/ksp-mods

https://github.com/zer0Kerbal

https://wiki.kerbalspaceprogram.com/wiki/Setting_up_Visual_Studio

https://wiki.kerbalspaceprogram.com/wiki/Tutorial:Creating_your_first_module