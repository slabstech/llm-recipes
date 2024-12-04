TTS -

- Download model from Huggingface
  - huggingface-cli download ai4bharat/indic-parler-tts

- Run with Docker compose
  - docker compose -f indic-tts-compose.yml  up --detach parler-tts-server

- Test output
  - kannada
    - curl -s -H "content-type: application/json" localhost:8000/v1/audio/speech -d '{"input": "ಉದ್ಯಾನದಲ್ಲಿ ಮಕ್ಕಳ ಆಟವಾಡುತ್ತಿದ್ದಾರೆ ಮತ್ತು ಪಕ್ಷಿಗಳು ಚಿಲಿಪಿಲಿ ಮಾಡುತ್ತಿವೆ."}' -o audio.mp3
    
  - hindi
    -  curl -s -H "content-type: application/json" localhost:8000/v1/audio/speech -d '{"input": "अरे, तुम आज कैसे हो?"}' -o audio.mp3

  - curl -s -H "content-type: application/json" localhost:8000/v1/audio/speech -d '{"input": "Hey, how are you?", "voice": "Feminine, speedy, and cheerfull"}' -o audio_2.mp3

 -  

--- 
TODO

- Create docker image
  - docker build -t indic-parler-tts .

- Run the container
  -  docker run -d -p 8000:8000 -v ~/.cache/huggingface:/root/.cache/huggingface parler-tts



-  huggingface-cli download  parler-tts/parler-tts-mini-expresso

- with slabstech/parler-tts
  - ai4bharat/indic-parler-tts
    - huggingface-cli download ai4bharat/indic-parler-tts
    - docker run --detach --volume ~/.cache/huggingface:/root/.cache/huggingface --publish 8000:8000 --env MODEL="ai4bharat/indic-parler-tts" slabstech/parler-tts-server
  - parler-tts/parler-tts-mini-expresso
    -  huggingface-cli download  parler-tts/parler-tts-mini-expresso
    - docker run --detach --volume ~/.cache/huggingface:/root/.cache/huggingface --publish 8000:8000 --env MODEL="parler-tts/parler-tts-mini-expresso" slabstech/parler-tts-server

- curl -s -H "content-type: application/json" localhost:8000/v1/audio/speech -d '{"input": "Hey, how are you?"}' -o audio.mp3
