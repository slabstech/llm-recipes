TODO - AudioBook Generator

- Production Server Requirements
  - Text to Sound Server 
    - Create docker container for Magnet/AudioGen  
  - Scene Editor UX
    - Edit the scenes and dialogs
    - Provide generate button for audio update
  - Full audiobook creator
    - Merge narrator, sound_effects and speaker dialogs audio files 
  - Build Evaluator for audiobook
    - Use Whisper ASR to verify audiobook generation for acceptance testing and avoid hallucination
  - Build AutoGen agent to build audiobooks from large corpus autonomously
  - Integrate with Django and database for Scene Editor tracking
  - Integrate Media Server with multimodal database for storing generated audio