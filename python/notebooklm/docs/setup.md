# Audiobook Creation Setup Guide

This guide will walk you through setting up your environment and necessary tools to create an audiobook using Python.

## Prerequisites

- **Python** installed on your system (preferably Python 3.8 or later)
- **Docker** installed and running

## Step-by-Step Setup

### 1. Create a Virtual Environment and Install Libraries

1. **Create a Virtual Environment:**
   ```sh
   python -m venv venv
   ```

2. **Activate the Virtual Environment:**
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```
   - On Windows:
     ```sh
     .\venv\Scripts\activate
     ```

3. **Install Required Libraries:**
   ```sh
   pip install -r requirements.txt
   ```

4. **For Pytorch Model Dev Users:**
   ```sh
   pip install -r pytorch-requirements.txt
   ```

### 2. Setup Ollama

1. **Start Docker Compose:**
   ```sh
   docker compose -f docker/llm-compose.yml up -d 
   ```

2. **Pull Necessary LLM Models:**
   ```sh
   ollama pull deepseek-r1:7b
   ollama pull qwen2.5
   ```


3. **Pull Necessary TTS and Audio Models:**
   To get started, download the following models using the Hugging Face CLI:

   ```sh
   huggingface-cli download parler-tts/parler-tts-mini-v1
   huggingface-cli download parler-tts/parler-tts-mini-v1.1
   huggingface-cli download parler-tts/parler-tts-mini-multilingual
   huggingface-cli download parler-tts/parler-tts-mini-multilingual-v1.1
   huggingface-cli download facebook/audiogen-medium
   huggingface-cli download facebook/audio-magnet-medium
   ```
4. **Start TTS Server for Speech Creation**
   ```sh
   docker compose -f docker/tts-server.yml up -d
   ```

5. **Start Audiocraft Server for Sound/Music Creation**
   ```sh
   docker compose -f docker/audiocraft-server.yml up -d 
   ```

### 4. Additional Tips

- **Environment Variables:**
  Ensure any required environment variables are set. You can use a `.env` file or set them directly in your terminal.

- **Dependencies:**
  Ensure all dependencies listed in `requirements.txt` and `pytorch-requirements.txt` are correct and up-to-date.

- **Docker Check:**
  Verify that Docker is running and the necessary containers are up and operational.

## Troubleshooting


- **Docker Issues:**
  Check Docker logs for any errors and ensure that the Docker daemon is running.

