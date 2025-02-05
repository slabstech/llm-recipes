# Architecture

## Overview

**TODO - 4th February**

### Objectives

- Create a magnet Docker container
- Input: text, duration
- UX: create wireframe, movable widgets like Jupyter notebook, add scene, speaker

### Workflow

1. **Parse**: Convert speech to LLM. Identify the emotion and update the speaker's voice description for Parler TTS.
2. **Cleanup**: Remove/cleanup words not meant to be read aloud.
3. **Create Workflow Diagram**: Visualize the process.
4. **Automate Steps**: Use agents for editing and novel generation based on inputs.

---

## Use Case

NotebookLM can be replicated using open-weight models with Python scripts from Notebookllama.

### Value Proposition

- **User Experience**: Create an intuitive UX for all users, including non-programmers.
- **Audio Books**: Enable users to convert their books, notes, and ideas into audio books.
- **Personal Journals**: Convert online journals into podcast format for personal consumption.
- **Learning**: Help users learn from past experiences and discover hidden insights over time.

### Current Progress

- Code for scripts is progressing well.
- **Next Steps**: Design a UX and make the tool available for others to experiment with.

---

## Microservice-Based Architecture

1. **TTS Container**: Text-to-speech service.
2. **Audio Gen Container**: Audio generation service.
3. **Parser Container**: LLM-based parsing service.
4. **Frontend Container**: User interface.
5. **Backend Container**: Application logic.
6. **Database Container**: Data storage.
7. **MongoDB Container**: Store audio from submitted notes.

### Queue Implementation

- Maintain GPU availability.
- Trigger tasks only upon successful completion of the previous task.

---

## Future Enhancements

1. **Scalability**: Ensure the architecture can scale with increasing user load.
2. **Modularity**: Make sure each microservice is independent and can be updated without affecting others.
3. **Security**: Implement robust security measures to protect user data.
4. **Documentation**: Provide comprehensive documentation for developers and users.
5. **Community Support**: Foster a community for user support and feature requests.
