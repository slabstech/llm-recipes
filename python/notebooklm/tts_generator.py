from pydub import AudioSegment
import os
import json
from tqdm import tqdm
import requests
from typing import List, Tuple

def update_voice_descriptions(language, file_content):
    # Define the replacement dictionary based on language
    replacements = {
        "de": {
            "Emma's voice is expressive,": "Nicole's voice is expressive,",
            "Leo's voice is deep and resonant,": "Michelle's voice is deep and resonant,"
        },
        "en": {
            "Emma's voice is expressive,": "Laura's voice is expressive,",
            "Leo's voice is deep and resonant,": "Mike's voice is deep and resonant,"
        }
    }

    # Check if the language is supported
    if language in replacements:
        for old_text, new_text in replacements[language].items():
            file_content = file_content.replace(old_text, new_text)
    else:
        print("Unsupported language")

    return file_content

def generate_speaker_audio(structured_scenes_file_path,language):


            # Load the JSON data from the file
    with open(structured_scenes_file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    file_content = file_content.replace("```json", "")
    file_content = file_content.replace("```", "")

    #language = "de"  
    #language = "en"
    updated_content = update_voice_descriptions(language, file_content)

    scenes_data_json = json.loads(updated_content)

    scenes_data = json.loads(scenes_data_json)

    scenes = scenes_data['scenes']
    # Ensure the 'generated' folder exists
    if not os.path.exists('generated'):
        os.makedirs('generated')

    #scenes = json.loads(scenes_data)['scenes']
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

    # Ensure the 'generated' folder exists
    if not os.path.exists('generated'):
        os.makedirs('generated')

    try:
        with open(narrator_file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()


        file_content = file_content.replace("```json", "")
        file_content = file_content.replace("```", "")
        scenes_data_narrator_json = json.loads(file_content)
        scenes_data_narrator = json.loads(scenes_data_narrator_json)
 
        scenes = scenes_data_narrator['scenes']
        for i, scene in enumerate(scenes, start=1):
            scene_title = scene['scene_title']
            narrator_description = scene['narrator_description']
            audio_segment = tts_server(narrator_description, "Jon's voice is monotone yet slightly fast in delivery, with a very close recording that almost has no background noise.")
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
    
        
def combine_audio_segments(structured_scenes_file_path='generated/structured_scene.json'):

        # Load the JSON data from the file
    with open(structured_scenes_file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    file_content = file_content.replace("```", "")

    scenes_data_json = json.loads(file_content)

    scenes_data = json.loads(scenes_data_json)

    scenes = scenes_data['scenes']
    final_audio = AudioSegment.silent(duration=0)

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
        final_audio += combined_audio
        combined_audio.export(f"generated/scene_{i}_{scene_title.replace(' ', '_')}_combined.mp3",
                              format="mp3",
                              bitrate="192k",
                              parameters=["-q:a", "0"])
    
    final_audio.export(f"full_audiobook_combined.mp3",
                              format="mp3",
                              bitrate="192k",
                              parameters=["-q:a", "0"])
    
def tts_server_batch(texts: List[str], speaker_descriptions) -> List[AudioSegment]:
    url = 'http://localhost:8000/v1/audio/speech_batch'
    payload = {
        'input': texts,
        'voice': speaker_descriptions
    }

    # Make the POST request
    response = requests.post(url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the audio files from the response
        audio_segments = []
        for i, audio_file in enumerate(response.json()):
            # Save each audio response as a WAV file
            with open(f'audio_{i}.mp3', 'wb') as f:
                f.write(audio_file)

            # Load the audio file using pydub
            audio = AudioSegment.from_mp3(f'audio_{i}.mp3')
            audio_segments.append(audio)

        return audio_segments
    else:
        raise Exception(f"Failed to generate audio: {response.status_code}")    
    
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

def speech_generator(language):

    # Define the path to the JSON file
    narrator_file_path = "generated/narrator_dialog.json"

    # Define the path to the JSON file
    speaker_dialog_file_path = "generated/speaker_dialog_voice.json"

    # Define the path to the JSON file
    structured_scenes_file_path = "generated/structured_scene.json"


    generate_narrator_voice(narrator_file_path)

    generate_speaker_audio(speaker_dialog_file_path, language)

    combine_audio_segments(structured_scenes_file_path)

    ''' Batch Speech Generatioon

    texts = ["Hey, how are you doing?", "I'm not sure how to feel about it."]
    speaker_descriptions = "A male speaker with a monotone and high-pitched voice is delivering his speech at a really low speed in a confined environment."

    audio_segments = tts_server_batch(texts, speaker_descriptions)
    for i, audio in enumerate(audio_segments):
        print(f"Audio {i}: {audio}")
    '''