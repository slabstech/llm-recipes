Audio Spectrogram Transformer (AST)

- Download dataset
    - ```huggingface-cli download MIT/ast-finetuned-audioset-10-10-0.4593```
- Setup python libraries
    - ```pip install -r requirements.txt```

- fast-api server
    - ```uvicorn ast_api:app --reload```

- Inference
    - ```curl -X POST "http://127.0.0.1:8000/predict" -F "file=@0_communication/0_communication.1.wav"```

    - ```curl -X POST "http://127.0.0.1:8000/predict" -F "file=@1_gunshot/1_gunshot.5.wav"```


 - Reference   
    - HF - https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593
        - 
    - Dataset
        - https://www.kaggle.com/datasets/wimccall/reduced-mad-dataset-military-audio-dataset
        - https://www.kaggle.com/datasets/junewookim/mad-dataset-military-audio-dataset
    - Code 
        - https://github.com/YuanGongND/ast
        - https://github.com/YuanGongND/ltu
    - https://huggingface.co/STMicroelectronics/yamnet
