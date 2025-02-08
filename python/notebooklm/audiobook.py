from tqdm import tqdm
from pydub import AudioSegment
import requests
import ast
import json
import os

def generate_podcast(podcast_text, speaker_1_description, speaker_2_description):
    final_audio = None

    for speaker, text in tqdm(ast.literal_eval(podcast_text), desc="Generating audiobook segments", unit="segment"):
        if speaker == "Emma":
            audio_segment = tts_server(text, speaker_1_description)
        else:  # Speaker 2
            audio_segment = tts_server(text, speaker_2_description)

        # Add to final audio
        if final_audio is None:
            final_audio = audio_segment
        else:
            final_audio += audio_segment

    final_audio.export("_audiobook_eng.mp3",
                      format="mp3",
                      bitrate="192k",
                      parameters=["-q:a", "0"])

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

def main():
    speaker_1_description = """
            Emma's voice is expressive and dramatic in delivery, speaking at a moderately fast pace with a very close recording that almost has no background noise.
        """
    speaker_2_description = """
            Leo's voice is deep and resonant, with a calm and authoritative tone. He speaks at a steady pace, ensuring clarity and precision in his delivery. The recording is clear with minimal background noise, providing a professional and engaging listening experience.
        """

    podcast_text = """
    [
        ('Emma', "So, Leo, what were you trying to show me here?"),
        ('Leo', "Patience, Emma. It's a bit... how should I say... next-level cool."),
        ('Emma', "Your surprises weren't always cool. Remember the super cave full of spiders."),
        ('Leo', "Hey, that was an adventure! And there are no spiders this time. I promise."),
    ]
    """

    podcast_text = podcast_text.strip()
    generate_podcast(podcast_text, speaker_1_description, speaker_2_description)

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


    generate_narrator_voice(scenes_data_narrator)

    generate_speaker_audio(scenes_data)

    combine_audio_segments(scenes_data)

if __name__ == "__main__":
    main()