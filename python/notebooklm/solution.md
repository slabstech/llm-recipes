Solution

- Two Ways to solve the challenge
  - Build with code and open weight models
  - Use existing 3rd party software

- Compare the outputs from both approaches to improve product
  - build an eval to measure what can be improved 

- Steps
  - Input Document
  - Detect Language / IndicLID for Indian language(Find for German/Euro languages)
  - Pre-process document / Cleanup via LLM parser to text/json format
    - Convert the script to Machine readable format
  - Identify all speaker and attribute their lines in DB/Graph
  - Identify Emotion/Tone/Background for Each speaker.
  - Create prompts for TTS-speaker based on conditions

- Evaluation
  - Use Whisper API for verifying output of TTS
    - Identify missing information and provide feedback to TTS generator 
    - How closely does it resemble the script provided.