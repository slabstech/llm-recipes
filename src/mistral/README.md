Mistral 

- Running inference and function calling
    - pip install mistral-inference
    - pip install mistral-common
    - export MISTRAL_MODEL=$HOME/mistral_models
    - mkdir -p $MISTRAL_MODEL
    - export 7B_DIR=$MISTRAL_MODEL/7B_instruct
    - wget https://models.mistralcdn.com/mistral-7b-v0-3/mistral-7B-Instruct-v0.3.tar
    - mkdir -p $7B_DIR
    - tar -xf Mistral-7B-v0.3-Instruct.tar -C $7B_DIR

- Reference
    - https://github.com/mistralai/mistral-inference