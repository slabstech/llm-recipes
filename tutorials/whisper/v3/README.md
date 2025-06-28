faster -whiserp

pip install httpx

curl --silent --remote-name https://raw.githubusercontent.com/speaches-ai/speaches/master/compose.yaml
curl --silent --remote-name https://raw.githubusercontent.com/speaches-ai/speaches/master/compose.cuda.yaml
export COMPOSE_FILE=compose.cuda.yaml

docker compose -f compose.cuda.yml up -d


curl -X 'POST' \
  'https://dwani-whisper.hf.space/v1/models/Systran/faster-whisper-small' \
  -H 'accept: application/json' \
  -d ''


curl -X 'POST' \
  'https://dwani-whisper.hf.space/v1/models/Systran/faster-whisper-large-v3' \
  -H 'accept: application/json' \
  -d ''


curl -X 'POST' \
  'https://dwani-whisper.hf.space/v1/models/speaches-ai/Kokoro-82M-v1.0-ONNX' \
  -H 'accept: application/json' \
  -d ''
