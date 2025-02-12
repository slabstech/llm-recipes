IndicTrans 2


- huggingface-cli download ai4bharat/indictrans2-indic-en-dist-200M

- pip install -r requirements.txt 

- Run with fastapi server
  - python translate_api.py

- Evaluate result
    - curl -X POST "http://localhost:8000/translate" \
     -H "Content-Type: application/json" \
     -d '{
           "sentences": [
               "जब मैं छोटा था, मैं हर रोज़ पार्क जाता था।",
               "हमने पिछले सप्ताह एक नई फिल्म देखी जो कि बहुत प्रेरणादायक थी।"
           ]
         }'

- https://huggingface.co/ai4bharat/indictrans2-indic-en-dist-200M

- https://github.com/AI4Bharat/IndicTrans2/tree/main/huggingface_interface



- REference
  - - pip install git+https://github.com/VarunGumma/IndicTransToolkit.git
