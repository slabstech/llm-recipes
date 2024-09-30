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


- TODO
    - Add cronjob to start all containers on reboot or crash