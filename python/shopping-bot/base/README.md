Setup for Shopping Bot

- Check for login 
    ```curl -X POST http://localhost:7860/login -H "Content-Type: application/json" -d '{"username": "user1", "password": "password123"}'```


- Voice UX
    - sudo apt install portaudio19-dev

- https for local certificates
    - sudo apt install openssl
    - pip install pyOpenSSL
    - openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
    - sudo apt install nginx