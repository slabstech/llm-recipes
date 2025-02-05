from utils.pdf_parser import parser_data
import os
from mistralai import Mistral

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



def get_structured_scene(scene_text):
    prompt_for_scene = """
You are given a script in a text format. Your task is to parse this script into a structured JSON format with the following requirements:

Scenes: Break the script down into distinct scenes.
Scene Title: Provide a descriptive title for each scene.
Background Music: Describe the background music or ambient sounds for each scene.
Sound Effects: List the specific sound effects that occur during each scene.
Dialogue: List the dialogue lines with the speaker's name clearly indicated.
"""
    structure_json = llm_parser(scene_text, prompt=prompt_for_scene)

    return structure_json

def main():
    print("Audiobook Creation from Script")
    local_filename = 'Skript-GoAudio-Eng.pdf'
    scene_text = parser_data(local_filename)

    structured_scene_json = get_structured_scene(scene_text=scene_text)
    print(structured_scene_json)


if __name__ == "__main__":
    main()
