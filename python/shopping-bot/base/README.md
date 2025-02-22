Setup for Shopping Bot



- local mock server
    - uvicorn mock_api:app --host 0.0.0.0 --port 7861

- ```curl -X POST -H "Content-Type: application/json" -d '{"username":"user1","password":"password123"}' http://localhost:7861/login```


- Use fircrawl to scrape data.

- Store data in db

- Voice UX
    - sudo apt install portaudio19-dev

- https for local certificates
    - sudo apt install openssl
    - pip install pyOpenSSL
    - openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
    - sudo apt install nginx

