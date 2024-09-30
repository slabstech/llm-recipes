DGX Server Maintenance

- Admin
    - Start openweb-ui + ollama container
        - cd server
        - docker compose -f docker-compose.yml up -d

    - Stop all AI containers
        - docker compose -f docker-compose.yml down

- Students
    - Steps to Run Docker Container
        - Build the container 
            - docker build -t test_code -f Dockerfile .
        - Run the container
            - docker run test_code

    - Continue-dev Setup
        - Install continue-dev extenstion on VSCode
        - Click on settings icon on the extension.
        - Replace the contents of default/existing config.json with 
            - file provided at [llm-recipes/python/dgx/students/config.json](https://github.com/slabstech/llm-recipes/tree/main/python/dgx/students/config.json)
            - It will connect to DGX instance or Local Ollama instance

- TODO
    - Add cronjob to start all containers on reboot or crash