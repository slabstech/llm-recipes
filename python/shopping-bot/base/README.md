Shopping Bot 


- Food Order Bot - https://huggingface.co/spaces/gaganyatri/food_order_bot

- redis server 
    - ```sudo apt install redis-server```

    - start local redis server
        - ```redis-server --port 8105```

- deployed source 
    - mock server -     https://huggingface.co/spaces/gaganyatri/mock_restaurant_api
    - food order bot - https://huggingface.co/spaces/gaganyatri/food_order_bot

- Mock server Endpoint -  "https://gaganyatri-mock-restaurant-api.hf.space/" 


- Check for login 
    ```curl -X POST http://localhost:7860/login -H "Content-Type: application/json" -d '{"username": "user1", "password": "password123"}'```


- Voice UX
    - sudo apt install portaudio19-dev

- hhtps
    - sudo apt install openssl
    - pip install pyOpenSSL
    - openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
    - sudo apt install nginx