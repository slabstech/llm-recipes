TTS -

- Download model from Huggingface
  - huggingface-cli download ai4bharat/indic-parler-tts

- Run with Docker compose
  - docker compose -f indic-tts-compose.yml  up --detach parler-tts-server

- Test output
  - curl -s -H "content-type: application/json" localhost:8000/v1/audio/speech -d '{"input": "Hey, how are you?"}' -o audio.mp3


--- 
TODO

- Create docker image
  - docker build -t indic-parler-tts .

- Run the container
  -  docker run -d -p 8000:8000 -v ~/.cache/huggingface:/root/.cache/huggingface parler-tts



-  huggingface-cli download  parler-tts/parler-tts-mini-expresso

- with fedirz/parler-tts
  - ai4bharat/indic-parler-tts
    - huggingface-cli download ai4bharat/indic-parler-tts
    - docker run --detach --volume ~/.cache/huggingface:/root/.cache/huggingface --publish 8000:8000 --env MODEL="ai4bharat/indic-parler-tts" fedirz/parler-tts-server
  - parler-tts/parler-tts-mini-expresso
    -  huggingface-cli download  parler-tts/parler-tts-mini-expresso
    - docker run --detach --volume ~/.cache/huggingface:/root/.cache/huggingface --publish 8000:8000 --env MODEL="parler-tts/parler-tts-mini-expresso" fedirz/parler-tts-server

- curl -s -H "content-type: application/json" localhost:8000/v1/audio/speech -d '{"input": "Hey, how are you?"}' -o audio.mp3
