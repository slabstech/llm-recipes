Setup with Vllm

- Creat account in huggingface > Profile > AccessToken > create new user Access token


docker run --gpus all \
    -e HF_TOKEN=$HF_TOKEN -p 8000:8000 \
    ghcr.io/mistralai/mistral-src/vllm:latest \
    --host 0.0.0.0 \
    --model mistralai/Mistral-7B-Instruct-v0.2

curl --location 'http://IP:Port/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data '{
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [
            {"role": "user", "content": "what minimun materials are necessary to build a Seed harvesting robot, show me how to arrange the parts"}
        ]
    }'