System Design


- Feature Requiremnts
    - Provide 30 sec sample for generated audio with speech, music and narrator for Public domain/Non-copyright book in 3 languages
        - English, German, Kannada

- System Requirements
    - Stream music per scene, Do not trigger full run on Script upload.
    - Run only parser and scene generator
    - Calculate estimated cost of Full run.  Make credits available for trial/demo.
    - Per Second basis cost calculator for on-demand GPU access and running. Check huggingface space with GPU

- Demo
    - Show sample doc in Indic Languages
        - Hindi, Kannada, Tamil and English
    - Provide non-copyrighted text
        - Use sarvam tts for audio generation
- TODO
  - 