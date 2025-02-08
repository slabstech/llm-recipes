from pydub import AudioSegment
import os
import json
from tqdm import tqdm
import requests

def generate_speaker_audio(scenes_data):
    # Ensure the 'generated' folder exists
    if not os.path.exists('generated'):
        os.makedirs('generated')

    scenes = json.loads(scenes_data)['scenes']
    for i, scene in enumerate(scenes, start=1):
        scene_title = scene['scene_title']
        dialogues = scene['dialogue']

        for dialogue in tqdm(dialogues, desc=f"Generating audio for scene {i}", unit="dialogue"):
            speaker = dialogue['speaker']
            line = dialogue['line']
            voice_description = dialogue['voice_description']
            audio_segment = tts_server(line, voice_description)
            audio_segment.export(f"generated/scene_{i}_{scene_title.replace(' ', '_')}_{speaker}.mp3",
                                 format="mp3",
                                 bitrate="192k",
                                 parameters=["-q:a", "0"])

def generate_narrator_voice(narrator_file_path='narrator_dialog.json'):


    #import json

    #narrator_file_path = 'path/to/narrator_dialog.json'

    try:
        with open(narrator_file_path, 'r') as file:
            file_content = file.read()
            print(file_content)  # Debug statement to check file content
            scenes_data_narrator = json.loads(file_content)
            print(type(scenes_data_narrator))  # Debug statement
            # Check if scenes_data_narrator is a dictionary
            if isinstance(scenes_data_narrator, dict):
                print(scenes_data_narrator['scenes'])
            else:
                print("Loaded data is not a dictionary")
    except FileNotFoundError:
        print(f"File not found: {narrator_file_path}")
    except json.JSONDecodeError:
        print("Error decoding JSON")
    except Exception as e:
        print(f"An error occurred: {e}")

    '''

    with open(narrator_file_path, 'r') as file:
        scenes_data_narrator = json.load(file)

    print(type(scenes_data_narrator))  # Debug statement
    #print(scenes_data_narrator) 

    print(scenes_data_narrator['scenes'])

    # Ensure the 'generated' folder exists
    if not os.path.exists('generated'):
        os.makedirs('generated')

    try:
        scenes = scenes_data_narrator['scenes']
        for i, scene in enumerate(scenes, start=1):
            scene_title = scene['scene_title']
            narrator_description = scene['narrator_description']
            audio_segment = tts_server(narrator_description, "Narrator's calm, soothing voice")
            audio_segment.export(f"generated/scene_{i}_{scene_title.replace(' ', '_')}_narrator.mp3",
                                format="mp3",
                                bitrate="192k",
                                parameters=["-q:a", "0"])
    except KeyError as e:
        print(f"KeyError: {e} - The key does not exist in the JSON data.")
    except TypeError as e:
        print(f"TypeError: {e} - Ensure the JSON data is correctly loaded into a dictionary.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    '''
        
def combine_audio_segments(scenes_data):
    scenes = json.loads(scenes_data)['scenes']
    for i, scene in enumerate(scenes, start=1):
        scene_title = scene['scene_title']
        combined_audio = AudioSegment.silent(duration=0)

        # Add narrator's voice
        narrator_file = f"generated/scene_{i}_{scene_title.replace(' ', '_')}_narrator.mp3"
        if os.path.exists(narrator_file):
            narrator_audio = AudioSegment.from_mp3(narrator_file)
            combined_audio += narrator_audio

        # Add dialogue
        for dialogue in scene['dialogue']:
            speaker = dialogue['speaker']
            dialogue_file = f"generated/scene_{i}_{scene_title.replace(' ', '_')}_{speaker}.mp3"
            if os.path.exists(dialogue_file):
                dialogue_audio = AudioSegment.from_mp3(dialogue_file)
                combined_audio += dialogue_audio

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

def speech_generator():

    # Define the path to the JSON file
    narrator_file_path = "generated/narrator_dialog.json"


    generate_narrator_voice(narrator_file_path)

    '''

    # Define the path to the JSON file
    speaker_dialog_file_path = "generated/speaker_dialog_voice.json"

    # Load the JSON data from the file
    with open(speaker_dialog_file_path, 'r') as file:
        scenes_data_speaker_dialog = json.load(file)

    '''

    # Define the path to the JSON file
    structured_scenes_file_path = "generated/structured_scene.json"

    # Load the JSON data from the file
    with open(structured_scenes_file_path, 'r') as file:
        script_scene_data = json.load(file)



    #generate_speaker_audio(scenes_data_speaker_dialog)

    combine_audio_segments(script_scene_data)