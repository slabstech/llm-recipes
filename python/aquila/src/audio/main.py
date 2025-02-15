import pandas as pd
import json 
import os
from mistralai import Mistral
import argparse


def llm_parser(text, prompt):
    try:
        data = text

        llm_prompt = f"Here is more data: {data}. Please answer the following question: {prompt}"            
        model = "mistral-large-latest"
        
        system_prompt_german ="Please provide a concise answer in German. Output the response in a human-readable way in German (with paragraphs, etc.)."
        messages = [
            {
                    "role": "system",
                    "content": "Please provide a concise answer in English. Output the response in the requested format. Do not explain the output. Do not add anything new"            
            },
            {               
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": llm_prompt
                    }
                ]
            }
        ]

        api_key = os.environ["MISTRAL_API_KEY"]
        client = Mistral(api_key=api_key)
        chat_response = client.chat.complete(model=model, messages=messages)
        content = chat_response.choices[0].message.content

        #print(content)
        return content
    except Exception as e:
        print(f"An error occurred: {e}")



def read_csv_analyse(file_name):
    df = pd.read_csv(file_name)

    # Get the column names (titles)
    titles = df.columns.tolist()

    # Get the count of all rows
    row_count = df.shape[0]

    # Print the titles and row count
    print(f"Titles: {titles}")
    print(f"Row count: {row_count}")

    if 'label' in titles and 'file_name' in titles:
        # Extract the 'label' and 'file_names' columns
        labels_and_file_names = df[['label', 'file_name']]

        # Define the chunk size
        chunk_size = 2500

        # Split the DataFrame into chunks of 2500 rows
        for start in range(0, len(labels_and_file_names), chunk_size):
            end = min(start + chunk_size, len(labels_and_file_names))
            chunk = labels_and_file_names[start:end]

            # Convert the chunk to a JSON string
            json_str = chunk.to_json(orient='records')

            # prompt = "From this labels and file_names provided , provide the count of files names, the different vehicle names related to military vehicles used for combat"


            prompt = "From this labels and file_names provided , provide the count of files names related to military vehicles used for combat"
            content = llm_parser(json_str, prompt=prompt)

            print(content)
            content = llm_parser(json_str, prompt=prompt)
            prompt = "From this labels and file_names provided , pprovide all the different helicopters used related to military vehicles used for combat"
            print(content)
            
           
            content = llm_parser(json_str, prompt=prompt)
            prompt = "From this labels and file_names provided , provide all the different fighter jets used related to military vehicles used for combat"
            print(content) 


def main():
    file_name = 'data/sorted_audio/Data.csv'
    read_csv_analyse(file_name=file_name)

if __name__ == "__main__":
    main()
