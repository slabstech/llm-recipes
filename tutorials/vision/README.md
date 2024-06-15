Vision Models

- Deployment
    - ollama container with moondream
        - docker compose -f vision-compose.yml up -d
        - docker ps 
        - docker exec -it <container-name> /bin/bash
        - ollama pull moondream
    - curl examples
        - curl http://localhost:11434/api/chat -d '{
  "model": "llava",
  "messages": [
    {
      "role": "user",
      "content": "What is in this image?",
      "images": [
        "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."
      ]
    }
  ]
}'

- curl http://localhost:11434/api/generate -d '{
  "model": "llava", 
  "prompt": "What is in this image?",
  "images": [
    "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."
  ]
}'



- llava
- Moondream
    - pip install transformers einops


Reference
    -  https://github.com/vikhyat/moondream
    - https://github.com/ollama/ollama/blob/main/docs/api.md#pull-a-model
    - 