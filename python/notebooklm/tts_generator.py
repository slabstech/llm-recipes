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

def generate_narrator_voice(scenes_data):
    # Ensure the 'generated' folder exists
    if not os.path.exists('generated'):
        os.makedirs('generated')

    scenes = json.loads(scenes_data)['scenes']
    for i, scene in enumerate(scenes, start=1):
        scene_title = scene['scene_title']
        narrator_description = scene['narrator_description']
        audio_segment = tts_server(narrator_description, "Narrator's calm, soothing voice")
        audio_segment.export(f"generated/scene_{i}_{scene_title.replace(' ', '_')}_narrator.mp3",
                             format="mp3",
                             bitrate="192k",
                             parameters=["-q:a", "0"])

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

    scenes_data_narrator = """
    {
        "scenes": [
            {
                "scene_title": "Forest Clearing",
                "narrator_description": "Wind whistles through the trees, leaves rustle quietly in the background. Birds chirp sporadically, then suddenly silence, as if something had startled them. A branch cracks in the distance. The echo of the cracking sound resonates through the air."
            }
        ]
    }
    """
    scenes_data = """
    {
        "scenes": [
            {
                "scene_title": "Forest Clearing",
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
                    }
                ]
            }
        ]
    }
    """
    generate_narrator_voice(scenes_data_narrator)

    generate_speaker_audio(scenes_data)

    combine_audio_segments(scenes_data)