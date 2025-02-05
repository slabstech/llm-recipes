# NotebookLM - Self-hosted Audiobook Platform

## Overview

NotebookLM is a self-hosted platform designed to create, manage, and enhance audiobooks. This platform leverages various tools and models to parse, transcribe, and improve manuscripts, ultimately providing high-quality audio content.

!["Audiobook Generator"](docs/images/audiobook-flow.jpg "Audiobook generator") 



- python audiobook.py
  - converts script pdf into structured scene json using mistral-large API.  
  - triggers Text to Speech server for speech/dialogs and store audio files in resources folder
  - triggers Text to Sound server for background sound/music and store audio files in resources folder
  - Combines generated audio from speech and sound modules and creates audibook for the provided script

## Features

### GoAudio

- **Challenge**: Understand the challenges involved in audio synchronization and transcription. [Read more](docs/challenge.md)
- **Solution**: Learn about the solutions we've implemented to overcome these challenges. [Read more](docs/solution.md)
- **Audio Sync**: Detailed guide on how to synchronize audio with text. [Read more](docs/audio-sync.md)

### Setup

Follow the [setup guide](docs/setup.md) to build an End-to-End platform for Notebook LLM.

### Steps

1. **PDF Parser**: Parse PDFs with a temperature setting of 0.
2. **Transcript Writer**: Transcribe audio with a temperature setting of 1 and a large context.

### Book Editor

The Book Editor is designed to help authors improve their manuscripts:

- **PDF Parsing**: Parse PDFs and provide suggestions for improvement.
- **PDF Update**: Update PDFs via markdown and self-correct the manuscript.
- **Evaluation**: Use Online API and Offline models for evaluation.

### Extra - NotebookLLama

- **On-Demand Audio**: Create on-demand audio for explaining topics via streaming.
- **Mini-Steps**: Branch information when new questions are requested/asked.
- **Implementation**: Implement ideas via a Python CLI first and conduct beta testing.
- **UX**: Add UX features when user testing is complete.

## Download Models

To get started, download the following models using the Hugging Face CLI:

```sh
huggingface-cli download parler-tts/parler-tts-mini-v1
huggingface-cli download facebook/audiogen-medium
```

## Reference

- **NotebookLLM**: Core documentation for NotebookLLM.
- **NotebookLlama**: Additional resources and use cases. [Learn more](https://github.com/meta-llama/llama-cookbook/tree/main/end-to-end-use-cases/NotebookLlama)
- **Code Security**: Best practices for code security. [Learn more](https://github.com/meta-llama/llama-cookbook/tree/main/end-to-end-use-cases/github_triage)

## Documentation

For more detailed information, refer to the following documents:

- [Challenge](docs/challenge.md)
- [Solution](docs/solution.md)
- [Audio Sync](docs/audio-sync.md)
- [Setup Guide](docs/setup.md)


-----

AI product experiment - Audiobook creator

https://github.com/slabstech/llm-recipes/tree/reasoning-context/python%2Fnotebooklm
contains the source code for the audiobook generator solution.

Current Status
1. Script parser - convert to scene structured json
2. TTS server - Parler-tts server to generate speech for dialogs in scenes
3. AudioGen module - Audiocraft/magnet background sound creator
4. Basic audiobook - linear worflow for full audio creation without scene logic

Documents
1. Approach: steps followed to solve the problem
https://github.com/slabstech/llm-recipes/blob/reasoning-context/python%2Fnotebooklm%2Fdocs%2Fapproach-challenge.md

2. Production Workflow : next steps to create production grade audiobook system.  https://github.com/slabstech/llm-recipes/blob/reasoning-context/python%2Fnotebooklm%2Fdocs%2Fworkflow.md


An experiment to build a production grade audiobook content generator system to help publishers build on their IP and reach larger audience.

---