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

4. **For Pytorch Users:**
   ```sh
   pip install -r tts-requirements.txt
   ```

### 2. Setup Ollama

1. **Start Docker Compose:**
   ```sh
   docker compose up -d llm-compose.yml
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
   huggingface-cli download facebook/audiogen-medium
   huggingface-cli download facebook/audio-magnet-medium
   ```

<!-- 
### 3. Run the PDF Parser and Prepare Data for TTS

1. **Run the PDF Parser:**
   ```sh
   python pdf-parser.py
   ```

### 4. Send Data to TTS (Text-to-Speech)

1. **Prepare the Text Data:**
   Ensure the output from the PDF parser is in a format suitable for your TTS engine.

2. **Run the TTS Script:**
   ```sh
   python tts-script.py
   ```
-->
### 4. Additional Tips

- **Environment Variables:**
  Ensure any required environment variables are set. You can use a `.env` file or set them directly in your terminal.

- **Dependencies:**
  Ensure all dependencies listed in `requirements.txt` and `tts-requirements.txt` are correct and up-to-date.

- **Docker Check:**
  Verify that Docker is running and the necessary containers are up and operational.

## Troubleshooting

- **Virtual Environment Issues:**
  If you encounter issues with the virtual environment, try deleting the `venv` directory and recreating it.

- **Docker Issues:**
  Check Docker logs for any errors and ensure that the Docker daemon is running.

- **Library Issues:**
  Ensure all libraries are compatible with your Python version. You can check compatibility in the respective library documentation.

## Conclusion

Following these steps should set up your environment to create an audiobook using Python. If you encounter any issues, refer to the troubleshooting section or seek help from the community.