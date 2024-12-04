TTS -


- Run with Docker compose
  - 

- Create docker image
  - docker build -t indic-parler-tts .

- Run the container
  -  docker run -d -p 8000:8000 -v ~/.cache/huggingface:/root/.cache/huggingface parler-tts

