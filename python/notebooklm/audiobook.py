from pdf_parser  import parser_data
import os
from mistralai import Mistral
import json
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
Do not provide additional strings to json
Ex. 
{
    "scenes": [
      {
        "scene_title": "Forest Clearing",
        "background_music": "Soft, ambient forest sounds with wind whistling, leaves rustling, and birds chirping sporadically.",
        "sound_effects": [
          "A branch cracks in the distance.",
          "Echo of the cracking sound."
        ],
        "dialogue": [
          {
            "speaker": "Emma",
            "line": "So, Leo, what were you trying to show me here?"
          },
          {
            "speaker": "Leo",
            "line": "Patience, Emma. It's a bit... how should I say... next-level cool."
          },
        ]
      }
    ]
  }
"""
    extracted_json = llm_parser(scene_text, prompt=prompt_for_scene)
    # File path for the JSON file
    file_path = 'structured_scene.json'

    # Write the cleaned JSON data back to the file
    with open(file_path, 'w') as json_file:
        json.dump(extracted_json, json_file, indent=4)

 
    # Read the JSON data from the file
    with open(file_path, 'r') as json_file:
        structure_json = json.load(json_file)

    return structure_json

def get_narrator_dialog(scene_text):
    '''
    prompt_for_scene = """
Your task is to parse this script into a structured JSON format with the following requirements:

  Analyze the following scene for an audiobook, providing dialogs for the main narrator only. Ensure the analysis captures the atmosphere, sound effects, and dialogue to create an immersive experience for the listener.",
  
"""
    '''
    prompt_for_scene = """
You are given a script for an audiobook that includes various scenes with background music, sound effects, and dialogue. Your task is to parse this script into a structured JSON format with the following requirements:

Extract the scene titles: Include the scene_title for each scene.
Describe the scenes: Provide a narrator_description for each scene that captures the atmosphere, sound effects, and actions, creating an immersive experience for the listener.
Exclude speaker dialogues: Do not include any dialogue spoken by the characters; focus solely on the narrator's description of the scene.
"""
    extracted_json = llm_parser(scene_text, prompt=prompt_for_scene)
    # File path for the JSON file
    file_path = 'narrator_dialog.json'

    # Write the cleaned JSON data back to the file
    with open(file_path, 'w') as json_file:
        json.dump(extracted_json, json_file, indent=4)

 
    # Read the JSON data from the file
    with open(file_path, 'r') as json_file:
        structure_json = json.load(json_file)

    return structure_json


def get_speaker_dialog_voice_desc(scene_text):
    prompt_for_scene = """
The task is to analyze the given script and update the voice descriptions for each speaker based on the scene. 
The initial voice descriptions provided a general overview of how each speaker sounds. 
The updated script includes detailed voice descriptions for each line of dialogue, 
incorporating the emotional nuances and specific tones relevant to each scene.
"""
    extracted_json = llm_parser(scene_text, prompt=prompt_for_scene)
    # File path for the JSON file
    file_path = 'speaker_dialog_voice.json'

    # Write the cleaned JSON data back to the file
    with open(file_path, 'w') as json_file:
        json.dump(extracted_json, json_file, indent=4)

 
    # Read the JSON data from the file
    with open(file_path, 'r') as json_file:
        structure_json = json.load(json_file)

    return structure_json


def get_sound_effects_time_stamps(scene_text):
    prompt_for_scene = """
Task: Create an Immersive Audiobook Experience

Objective: To create a detailed and immersive audiobook experience by structuring scenes with specific timestamps and durations for background music, sound effects, and dialogue. This will ensure a dynamic and engaging listening experience.

Requirements:

Scene Structure: Each scene should include:

Scene Title
Background Music with description, timestamp, and duration
Sound Effects with description, timestamp, and duration
Dialogue with speaker, line, timestamp, and duration
Timestamps and Durations:

Provide precise timestamps for when each background music, sound effect, and dialogue line starts.
Include the duration for each background music, sound effect, and dialogue line.
JSON Format: The final output should be in JSON format for easy integration into an audiobook production system.

  
"""
    extracted_json = llm_parser(scene_text, prompt=prompt_for_scene)
    # File path for the JSON file
    file_path = 'sound_effects_timestamp.json'

    # Write the cleaned JSON data back to the file
    with open(file_path, 'w') as json_file:
        json.dump(extracted_json, json_file, indent=4)

 
    # Read the JSON data from the file
    with open(file_path, 'r') as json_file:
        structure_json = json.load(json_file)

    return structure_json


def main():
    print("Audiobook Creation from Script")
    local_filename = 'Skript-GoAudio-Eng.pdf'
    scene_text = parser_data(local_filename)

    structured_scene_json = get_structured_scene(scene_text=scene_text)

    print(structured_scene_json)


    narrator_dialog = get_narrator_dialog(structured_scene_json)


    print(narrator_dialog)

    speaker_voice_dialog = get_speaker_dialog_voice_desc(structured_scene_json)

    print(speaker_voice_dialog)

    sound_effects_timestamps = get_sound_effects_time_stamps(structured_scene_json)

    print(sound_effects_timestamps)

if __name__ == "__main__":
    main()
