# NotebookLM - Self-hosted Audiobook Generation Platform

<div style="display: flex;">
  <div style="flex: 1; padding: 10px;">
    <img src="docs/images/book-1.jpg" alt="Music from Book" style="width: 50%;">
  </div>
  <div style="flex: 1; padding: 10px;">
    <img src="docs/images/book-2.jpg" alt="Voices from Book" style="width: 50%;">
  </div>
</div>

## Overview

NotebookLM is a self-hosted platform designed to create, manage, and enhance audiobooks. This platform leverages various tools and models to parse, transcribe, and improve manuscripts, ultimately providing high-quality audio content.


!["Audiobook Generator"](docs/images/audiobook-flow.jpg "Audiobook generator") 

- **Roadmap**: Product Launch Roadmap [Read more](docs/roadmap.md)



### Steps 
- python audiobook.py
  - converts script pdf into structured scene json using mistral-large API.  
  - triggers Text to Speech server for speech/dialogs and store audio files in resources folder
  - triggers Text to Sound server for background sound/music and store audio files in resources folder
  - Combines generated audio from speech and sound modules and creates audibook for the provided script

!["Script Parser"](docs/images/script-parser.jpg "Script Parser") 

- **Prompts for Audiobook**: Creating a storyline using prompts [Read more](docs/prompts.md)



## Current Status
1. Script parser - convert to scene structured json
2. TTS server - Parler-tts server to generate speech for dialogs in scenes
3. AudioGen module - Audiocraft/magnet background sound creator
4. Basic audiobook - linear worflow for full audio creation without scene logic

## Documentation

- **Challenge**: project challenge. [Read more](docs/challenge.md)
- **Approach**: Approach in solving the problem. [Read more](docs/approach-challenge.md)
- **Workflow**: Worflow for audiobook generation. [Read more](docs/workflow.md)
- **Setup**: Follow the [setup guide](docs/setup.md) to build an End-to-End platform for Audibook Generation/Notebook LLM.
- **UX**: UX design for Audiobook generation [Read more](docs/ux.md)
- **Database Schema**: Schema for Scene Editing and Media content [Read more](docs/database_schema.md)

An experiment to build a production grade audiobook content generator system to help publishers build on their IP and reach larger audience.

## Reference

- **NotebookLlama**: Additional resources and use cases. [Learn more](https://github.com/meta-llama/llama-cookbook/tree/main/end-to-end-use-cases/NotebookLlama)

- TTS - Generation Docker - https://github.com/ashleykleynhans/tts-generation-docker
- https://github.com/rsxdalv/tts-generation-webui
- WishList - RTX 4090 GPU based computer for building End to End product inhouse. Buy Me [Razer Blade 18](https://www.notebooksbilliger.de/razer+blade+18+mercury+848789) or [ROG Zephyrus M16 ](https://www.notebooksbilliger.de/rog+zephyrus+m16+gu604vy+nm042w+847870)