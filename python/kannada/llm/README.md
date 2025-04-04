Kannada LLM


# Build and run
docker build -t krutrim-api . && docker run -p 8000:8000 krutrim-api

# Test endpoints
curl -X POST "http://localhost:8000/v1/chat/completions" \
-H "Content-Type: application/json" \
-d '{
  "messages": [{"role": "user", "content": "Explain quantum computing"}],
  "max_tokens": 256
}'
