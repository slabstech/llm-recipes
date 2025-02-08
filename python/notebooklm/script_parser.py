import json 
import os
from mistralai import Mistral
import argparse
from pdf_parser  import parser_data



def load_script_prompts(file_path):
    with open(file_path, 'r') as file:
        script_prompts = json.load(file)
    return script_prompts

    
def load_script_prompts(file_path):
    with open(file_path, 'r') as file:
        script_prompts = json.load(file)
    return script_prompts

def get_prompt_by_task_name_and_language(script_prompts, task_name, language):
    for task in script_prompts["tasks"]:
        if task["task_name"] == task_name:
            for prompt in task["prompts"]:
                if prompt["language"] == language:
                    return prompt["prompt"]
    return None

def get_structured_scene(scene_text, script_prompts, language):
    prompt_for_scene = get_prompt_by_task_name_and_language(script_prompts, "Script parser into Structured scene", language)
    extracted_json = llm_parser(scene_text, prompt=prompt_for_scene)
    # File path for the JSON file
    file_path = 'generated/structured_scene.json'

    # Write the cleaned JSON data back to the file
    with open(file_path, 'w') as json_file:
        json.dump(extracted_json, json_file, indent=4)

    # Read the JSON data from the file
    with open(file_path, 'r') as json_file:
        structure_json = json.load(json_file)

    return structure_json

def get_narrator_dialog(scene_text, script_prompts, language):
    prompt_for_scene = get_prompt_by_task_name_and_language(script_prompts, "Prompt parser for narrator description", language)
    extracted_json = llm_parser(scene_text, prompt=prompt_for_scene)
    # File path for the JSON file
    file_path = 'generated/narrator_dialog.json'

    # Write the cleaned JSON data back to the file
    with open(file_path, 'w') as json_file:
        json.dump(extracted_json, json_file, indent=4)

    # Read the JSON data from the file
    with open(file_path, 'r') as json_file:
        structure_json = json.load(json_file)

    return structure_json

def get_speaker_dialog_voice_desc(scene_text, script_prompts, language):
    prompt_for_scene = get_prompt_by_task_name_and_language(script_prompts, "Speaker Dialog Prompt for Parser", language)
    extracted_json = llm_parser(scene_text, prompt=prompt_for_scene)
    # File path for the JSON file
    file_path = 'generated/speaker_dialog_voice.json'

    # Write the cleaned JSON data back to the file
    with open(file_path, 'w') as json_file:
        json.dump(extracted_json, json_file, indent=4)

    # Read the JSON data from the file
    with open(file_path, 'r') as json_file:
        structure_json = json.load(json_file)

    return structure_json

def get_sound_effects_time_stamps(scene_text, script_prompts, language):
    prompt_for_scene = get_prompt_by_task_name_and_language(script_prompts, "Prompt for background music and sound effect with timestamps", language)
    extracted_json = llm_parser(scene_text, prompt=prompt_for_scene)
    # File path for the JSON file
    file_path = 'generated/sound_effects_timestamp.json'

    # Write the cleaned JSON data back to the file
    with open(file_path, 'w') as json_file:
        json.dump(extracted_json, json_file, indent=4)

    # Read the JSON data from the file
    with open(file_path, 'r') as json_file:
        structure_json = json.load(json_file)

    return structure_json
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


def script_parser(language, file_name):
    print("Audiobook Creation from Script")
    scene_text = parser_data(file_name)

    # Ensure the 'generated' folder exists
    if not os.path.exists('generated'):
        os.makedirs('generated')

    # Load script prompts
    script_prompts = load_script_prompts('docs/script_prompts_eu.json')

    structured_scene_json = get_structured_scene(scene_text=scene_text, script_prompts=script_prompts, language=language)
    
    narrator_dialog = get_narrator_dialog(structured_scene_json, script_prompts=script_prompts, language=language)

    speaker_voice_dialog = get_speaker_dialog_voice_desc(structured_scene_json, script_prompts=script_prompts, language=language)

    #sound_effects_timestamps = get_sound_effects_time_stamps(structured_scene_json, script_prompts=script_prompts, language=language)

    '''
    print(structured_scene_json)

    print(narrator_dialog)
    print(speaker_voice_dialog)

    print(sound_effects_timestamps)

    '''