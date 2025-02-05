Workflow - Optimised for Production

1. User upload PDF/Doc to Main Page
2. Entry is made in DB for Async Main Actions Run
3. Entry is made into celery for creating async calls to 
  - Script parser - LLM : Large Context
  - Script is split into Sessions and session is split into background music, narrator and speakers
  - Calls are executed Session by session for Human feedback.
  - Async calls for audio gen for backgound music with script-id, session-id, background-music-id
  - Async call on TTS service is made for each session for narraor, different speakers with session-id, speaker-turn-id
  - Based on GPU availability, Async call's can be run in linear or parallel ( Later optimisation problem) 
4. Script Parser
  - Using structured outputs, splits the scripts into different session based on template. Scene, Background Score, Conversation
  - Background score is split into distinct sounds and approximate duration for audio generation
  - Conversation is analysed and Voice-description for each session is updated based on Inputs. 
    Ex 
    - Emma (whispering)
        - Leo… What have you done?
    - Leo (excited)
        - I think… we just discovered something big.
  - Narrator voice is chosen and given a distinct personality based on user choice.
