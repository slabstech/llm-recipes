from tqdm import tqdm
from pydub import AudioSegment
import requests
import ast
import json
import os
from mistralai import Mistral
import 
from pdf_parser  import parser_data

def load_script_prompts(file_path):
    with open(file_path, 'r') as file:
        script_prompts = json.load(file)
    return script_prompts

def generate_speaker_audio(scenes_data):
    scenes = json.loads(scenes_data)['scenes']
    for i, scene in enumerate(scenes, start=1):
        scene_title = scene['scene_title']
        dialogues = scene['dialogue']

        for dialogue in tqdm(dialogues, desc=f"Generating audio for scene {i}", unit="dialogue"):
            speaker = dialogue['speaker']
            line = dialogue['line']
            voice_description = dialogue['voice_description']
            audio_segment = tts_server(line, voice_description)
            audio_segment.export(f"scene_{i}_{scene_title.replace(' ', '_')}_{speaker}.mp3",
                                 format="mp3",
                                 bitrate="192k",
                                 parameters=["-q:a", "0"])

def generate_narrator_voice(scenes_data):
    scenes = json.loads(scenes_data)['scenes']
    for i, scene in enumerate(scenes, start=1):
        scene_title = scene['scene_title']
        narrator_description = scene['narrator_description']
        audio_segment = tts_server(narrator_description, "Narrator's calm, soothing voice")
        audio_segment.export(f"scene_{i}_{scene_title.replace(' ', '_')}_narrator.mp3",
                             format="mp3",
                             bitrate="192k",
                             parameters=["-q:a", "0"])

def combine_audio_segments(scenes_data):
    scenes = json.loads(scenes_data)['scenes']
    for i, scene in enumerate(scenes, start=1):
        scene_title = scene['scene_title']
        combined_audio = AudioSegment.silent(duration=0)

        # Add dialogue
        for dialogue in scene['dialogue']:
            speaker = dialogue['speaker']
            dialogue_file = f"scene_{i}_{scene_title.replace(' ', '_')}_{speaker}.mp3"
            if os.path.exists(dialogue_file):
                dialogue_audio = AudioSegment.from_mp3(dialogue_file)
                combined_audio += dialogue_audio

        # Add narrator's voice
        narrator_file = f"scene_{i}_{scene_title.replace(' ', '_')}_narrator.mp3"
        if os.path.exists(narrator_file):
            narrator_audio = AudioSegment.from_mp3(narrator_file)
            combined_audio += narrator_audio

        # Export combined audio
        combined_audio.export(f"scene_{i}_{scene_title.replace(' ', '_')}_combined.mp3",
                              format="mp3",
                              bitrate="192k",
                              parameters=["-q:a", "0"])

def tts_server(text, speaker_description):
    url = 'http://localhost:8000/v1/audio/speech'

    payload = {
        'input': text,
        'voice': speaker_description
    }

    # Make the POST request
    response = requests.post(url, json=payload)
    # Check if the request was successful
    if response.status_code == 200:
        # Save the audio response as a WAV file
        # Create a file-like object with the audio data
        with open('audio.mp3', 'wb') as f:
            f.write(response.content)

            # Load the audio file using pydub
        audio = AudioSegment.from_mp3("audio.mp3")

        # Convert the audio to a NumPy array
        return audio
    
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
    file_path = 'structured_scene.json'

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
    file_path = 'narrator_dialog.json'

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
    file_path = 'speaker_dialog_voice.json'

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
    file_path = 'sound_effects_timestamp.json'

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

def main():

    scenes_data_narrator = """
    {
        "scenes": [
            {
                "scene_title": "Forest Clearing",
                "narrator_description": "Wind whistles through the trees, leaves rustle quietly in the background. Birds chirp sporadically, then suddenly silence, as if something had startled them. A branch cracks in the distance. The echo of the cracking sound resonates through the air."
            },
            {
                "scene_title": "Tree Door",
                "narrator_description": "An old tree stands before them, its trunk rough and full of grooves. In the middle there is a small wooden door, almost invisible in the twilight. The door creaks loudly as Leo pushes it open, like an old, heavy wooden cupboard. A faint, echoing sound follows as the door swings back against the trunk."
            },
            {
                "scene_title": "Narrow Corridor",
                "narrator_description": "Drops of water trickle in the distance, a steady sound like a broken water pipe. Footsteps on wet ground produce a dull, muddy sound. Small, flickering lights hang from the ceiling like fireflies, casting dancing shadows on the walls."
            },
            {
                "scene_title": "Cave with Lightcore",
                "narrator_description": "A large, glowing artifact floats in the center, surrounded by a deep, vibrating hum. The hum is barely audible, but you can feel it in your chest. The humming becomes more intense, deeper, and it sounds as if the floor is vibrating slightly. A high tone mixes into the roar, slowly increasing and sounding almost like the roar of an engine. The light of the artifact flickers. A dull hum fills the air, almost like an electric charge. The humming gets louder and a bright beam of light suddenly shoots into the darkness. A deep, vibrating hum that runs through the room ends abruptly. The cave becomes silent, except for a faint crackling sound, like static electricity. A quiet humming starts again, faint and rhythmic. Somewhere water drips into a small puddle. A high, whirring sound suddenly breaks through the silence before it dies away again. A soft knock comes from somewhere in the darkness, like an echo returning."
            }
        ]
    }
    """
    scenes_data = """
    {
        "scenes": [
            {
                "scene_title": "Forest Clearing",
                "background_music": "Wind whistles through the trees, leaves rustle quietly in the background. Birds chirp sporadically, then suddenly silence, as if something had startled them.",
                "sound_effects": [
                    "A branch cracks in the distance.",
                    "Echo of the cracking sound."
                ],
                "dialogue": [
                    {
                        "speaker": "Emma",
                        "line": "So, Leo, what were you trying to show me here?",
                        "voice_description": "Emma's voice is expressive and dramatic, with a hint of curiosity and impatience, speaking at a moderately fast pace."
                    },
                    {
                        "speaker": "Leo",
                        "line": "Patience, Emma. It's a bit... how should I say... next-level cool.",
                        "voice_description": "Leo's voice is deep and resonant, with a calm and authoritative tone, speaking at a steady pace with a hint of excitement."
                    },
                    {
                        "speaker": "Emma",
                        "line": "Your surprises weren't always cool. Remember the \\"super cave\\" full of spiders.",
                        "voice_description": "Emma's voice is expressive and dramatic, with a touch of sarcasm and caution."
                    },
                    {
                        "speaker": "Leo",
                        "line": "Hey, that was an adventure! And there are no spiders this time. I promise.",
                        "voice_description": "Leo's voice is deep and resonant, with a calm and reassuring tone, speaking at a steady pace."
                    }
                ]
            },
            {
                "scene_title": "Tree Door",
                "background_music": "",
                "sound_effects": [
                    "An old tree stands before them, its trunk rough and full of grooves. In the middle there is a small wooden door, almost invisible in the twilight.",
                    "The door creaks loudly as Leo pushes it open, like an old, heavy wooden cupboard. A faint, echoing sound follows as the door swings back against the trunk."
                ],
                "dialogue": [
                    {
                        "speaker": "Emma",
                        "line": "What the...? Is that a real door? In a tree? Seriously?",
                        "voice_description": "Emma's voice is expressive and dramatic, with a mix of surprise and disbelief, speaking at a moderately fast pace."
                    },
                    {
                        "speaker": "Leo",
                        "line": "Yep! Now wait until you see what's behind it. Come with me!",
                        "voice_description": "Leo's voice is deep and resonant, with a tone of excitement and anticipation, speaking at a steady pace."
                    },
                    {
                        "speaker": "Emma",
                        "line": "I have a strange feeling about this...",
                        "voice_description": "Emma's voice is expressive and dramatic, with a touch of caution and concern."
                    },
                    {
                        "speaker": "Leo",
                        "line": "Strange feeling? This is adventure, Emma! Come on!",
                        "voice_description": "Leo's voice is deep and resonant, with a tone of encouragement and enthusiasm, speaking at a steady pace."
                    }
                ]
            },
            }
        ]
    }
    """
    '''
    print("Audiobook Creation from Script")
    local_filename = 'audiobook/resources/Skript-GoAudio-Eng.pdf'
    scene_text = parser_data(local_filename)

    # Load script prompts
    script_prompts = load_script_prompts('script_prompts_eu.json')

    structured_scene_json = get_structured_scene(scene_text=scene_text, script_prompts=script_prompts, language=language)
    print(structured_scene_json)

    narrator_dialog = get_narrator_dialog(structured_scene_json, script_prompts=script_prompts, language=language)
    print(narrator_dialog)

    speaker_voice_dialog = get_speaker_dialog_voice_desc(structured_scene_json, script_prompts=script_prompts, language=language)
    print(speaker_voice_dialog)

    sound_effects_timestamps = get_sound_effects_time_stamps(structured_scene_json, script_prompts=script_prompts, language=language)
    print(sound_effects_timestamps)

    '''
    generate_narrator_voice(scenes_data_narrator)

    generate_speaker_audio(scenes_data)

    combine_audio_segments(scenes_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audiobook Creation from Script")
    parser.add_argument('--language', type=str, default='en', help='Language code for the prompts (e.g., en, fr, de, es, it, nl, pt, sv)')
    args = parser.parse_args()
    main(args.language)