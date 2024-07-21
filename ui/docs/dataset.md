Dataset

 - Setup 
    - kaggle
        - Create a kaggle account
        - Download the token from https://www.kaggle.com/settings
            - Create a new token, kaggle.json is downloaded
            - Ensure kaggle.json is in the location ~/.kaggle/kaggle.json to use the API.
                - cd $HOME
                - mkdir .kaggle
                - mv Downloads/kaggle.json .kaggle/
                - chmod 600 $HOME/.kaggle/kaggle.json
        - Install kaggle in python environment
            - pip install kaggle
    - huggingface
        - Create a huggingface account
    

- Download the dataset from kaggle
    - kaggle datasets download -d sriramr/fruits-fresh-and-rotten-for-classification
    - kaggle datasets download -d swoyam2609/fresh-and-stale-classification
    - kaggle datasets download -d swoyam2609/scrapped-image-dataset-of-fresh-and-rotten-fruits


- Create eval
    - mkdir -p dataset dataset/dataset_1 dataset/dataset_2 dataset/dataset_3
        - unzip fresh-and-stale-classification.zip -d dataset/dataset_1
        - unzip fruits-fresh-and-rotten-for-classification.zip -d dataset/dataset_2
        - unzip scrapped-image-dataset-of-fresh-and-rotten-fruits.zip -d dataset/dataset_3

- References
    - kaggle
        - https://www.kaggle.com/datasets/sriramr/fruits-fresh-and-rotten-for-classification
        - https://www.kaggle.com/datasets/swoyam2609/fresh-and-stale-classification
        - https://www.kaggle.com/datasets/moltean/fruits/data
        - https://www.kaggle.com/datasets/sriramr/apples-bananas-oranges
    - hugging face
        - https://huggingface.co/datasets/jojogo9/freshness
        - https://huggingface.co/datasets/jojogo9/freshness_of_fruits_and_veges_256
        - https://huggingface.co/datasets/elonmuskceo/parquet-fruits
        - https://huggingface.co/datasets/BangumiBase/fruitsbasket/blob/main/all.zip
        - https://huggingface.co/datasets/Nicollas563/LuffyAI_Blox_Fruits
        - https://huggingface.co/datasets/henningheyen/LVIS_Fruits_And_Vegetables
        - https://huggingface.co/datasets/VinayHajare/Fruits-30
        - https://huggingface.co/datasets/PedroSampaio/fruits-360