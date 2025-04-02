FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && apt-get install -y --no-install-recommends wget gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Download the model
RUN mkdir /app/models && wget -O /app/models/krutrim-ai-labs_Krutrim-2-instruct-Q6_K.gguf  "https://huggingface.co/bartowski/krutrim-ai-labs_Krutrim-2-instruct-GGUF/resolve/main/krutrim-ai-labs_Krutrim-2-instruct-Q6_K.gguf"

# Copy application code
COPY main.py .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
