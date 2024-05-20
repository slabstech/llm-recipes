Personal - Digital Twin

An attempt to build a Digital twin of your Persona.

- Idea 
    - Generate dataset of all Online activity and notes
    - Create tokens of your dataset
    - FineTune/Post-training of LLM models using LoRA/RAG
    - Create an end-point with your own Persona

- Steps
    - Convert all your markdown to pdf
        - https://slabstech.com/books/ or https://github.com/slabstech/slabstech.github.io/tree/main/assets/pdf 
    - Create tokens using tiktoken or minbpe
        - https://github.com/openai/tiktoken
        - https://github.com/karpathy/minbpe 
    - Finetune / post-training of LLM


- Work
    - pip install requests
    - pip install tiktoken
    - pip install --upgrade openai
    - pip install mistral-common    