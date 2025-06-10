# LLM Recipes

## Introduction

LLM Recipes is a collection of projects and tools aimed at creating decision agents with various capabilities such as speech, vision, and text search. This repository includes different versions of the project, each with unique features and functionalities.

## Installation

To get started with LLM Recipes, follow these steps:

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/sachinsshetty/llm-recipes.git
   cd llm-recipes
   ```

2. **Set Up Environment:**
   - Follow the instructions in the [clean-ubuntu-setup.md](docs/clean-ubuntu-setup.md) for a clean install of Ubuntu, Docker, and Nvidia requirements.
   - For ChatUI setup, refer to [ollama-open-webui.md](docs/ollama-open-webui.md).
   - For Code CoPilot setup, refer to [code-pair.md](docs/code-pair.md).

## Usage

Detailed usage instructions for each project version can be found in the respective documentation links provided in the table below.

## Projects

| Version | Concept                                | Status     | Tech                        |
|---------|----------------------------------------|------------|-----------------------------|
| v0.11   | [Voice - Shopping Bot](python/shopping-bot)           | In-progress | Python                     |
| v0.10   | [Multi-modal Agents](python/aquila/agents/)            | In-progress | Python                     |
| v0.9    | [NoteBook LLama](python/notebooklm)                   | Complete   | Python + TTS               |
| v0.8    | [Quantisation](tutorial/llama.cpp/)                   | Paused     | llama.cpp                  |
| v0.7    | [On-device Mobile](tutorial/android/)                  | Paused     | Android + TF lite          |
| v0.6    | [UI](UI)                                              | Complete   | Typescript - [link](https://sanjeevini.me) |
| v0.5    | [Indoor Maps + v0.4](python/reconaissance/reconaissance.py) | Paused     | ROS2                       |
| v0.4    | [Image/Scene Recognition + v0.3](python/assistant/vision_query.py) | Complete   | llava/moondream            |
| v0.3    | [Speech Output + v0.2](python/assistant/speech-to-speech-inference.py) | Complete   | coqui tts + v1             |
| v0.2    | [Speech Input + v0.1](python/assistant/voice_api_interface.py) | Complete   | whisper + ffpmeg + v0      |
| v0.1    | [Text Query + API Calls](python/assistant/api_interface.py) | Complete   | mistral7B-v0.3 + ollama + RestAPI |

## Base Setup

### ChatUI
- **Tools:** ollama, open-webui, mistral-7B, docker
- **Setup + Documentation:** [ollama-open-webui.md](docs/ollama-open-webui.md)

### Code CoPilot
- **Tools:** vscode, continue, ollama, mistral-7B
- **Setup Document:** [code-pair.md](docs/code-pair.md)

## Tutorials

- [Tutorials](docs/tutorials.md)

## Extra

- [Clean Install](docs/clean-ubuntu-setup.md) of Ubuntu + Docker + Nvidia Requirements

## Applications

### Reconnaissance with Drone
- Use drones to create real-time insights for warehouse management and home security.

![Reconnaissance](python/reconaissance/reconaissance.drawio.png "Reconnaissance")

## Upcoming Challenges

- [Hackathons](docs/hackathons.md)

## Dependencies

- Python
- Docker
- TensorFlow Lite
- ROS2
- LLama.cpp
- Coqui TTS
- Whisper
- Mistral7B
- Ollama
- Typescript

## FAQs

- **Q: How do I contribute to the project?**
  - **A:** Please refer to the [Contributing Guidelines](docs/contributing.md).

- **Q: What license is the project under?**
  - **A:** This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Screenshots

![Screenshot 1](path/to/screenshot1.png)
![Screenshot 2](path/to/screenshot2.png)

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your-repo/llm-recipes/tags).

## Acknowledgments

- Thanks to the contributors and maintainers of the third-party libraries used in this project.

## Contact

For any questions or support, please contact [your-email@example.com](mailto:your-email@example.com) or join our [Discord Server](https://discord.gg/h8ygUwvw).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.