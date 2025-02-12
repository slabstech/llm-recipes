IndicTrans 2

- Indic to English
    - huggingface-cli download ai4bharat/indictrans2-indic-en-dist-200M

- English to Indic
    - huggingface-cli download ai4bharat/indictrans2-en-indic-dist-200M
- Indic to Indic
  - huggingface-cli download ai4bharat/indictrans2-indic-indic-dist-320M

- pip install -r requirements.txt 

- Run with fastapi server 
  - ``` uvicorn translate_api:app --host 0.0.0.0 --port 8000```

  - ```python translate_api.py```

- Evaluate result

    - English to Kannada
    ```
    curl -X POST "http://localhost:8000/translate" \
     -H "Content-Type: application/json" \
     -d '{
           "sentences": ["Hello, how are you?", "Good morning!"],
           "src_lang": "eng_Latn",
           "tgt_lang": "kan_Knda"
         }'
    ```


    - Kannada to English
    ```
    curl -X POST "http://localhost:8000/translate" \
     -H "Content-Type: application/json" \
     -d '{
           "sentences": ["ನಮಸ್ಕಾರ, ಹೇಗಿದ್ದೀರಾ?", "ಶುಭೋದಯ!"],
           "src_lang": "kan_Knda",
           "tgt_lang": "eng_Latn"
         }'
    ```

    - Hindi to English
    ```
    curl -X POST "http://localhost:8000/translate" \
        -H "Content-Type: application/json" \
        -d '{
            "sentences": ["नमस्ते दुनिया", "आप कैसे हो?"],
            "src_lang": "hin_Deva",
            "tgt_lang": "eng_Latn"
            }'
    ```


- Reference
    - https://huggingface.co/ai4bharat/indictrans2-indic-en-dist-200M
    - https://github.com/AI4Bharat/IndicTrans2/tree/main/huggingface_interface
    - pip install git+https://github.com/VarunGumma/IndicTransToolkit.git
