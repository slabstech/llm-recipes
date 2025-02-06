from tqdm import tqdm
from pydub import AudioSegment
import requests

def generate_podcast(podcast_text, speaker_1_description,speaker_2_description ):
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

import ast

def main():
    '''
    speaker_1_description = """
            Laura's voice is expressive and dramatic in delivery, speaking at a moderately fast pace with a very close recording that almost has no background noise.
        """
    speaker_2_description = """
            Michael's voice is deep and resonant, with a calm and authoritative tone. He speaks at a steady pace, ensuring clarity and precision in his delivery. The recording is clear with minimal background noise, providing a professional and engaging listening experience.
        """

    podcast_text = """
    [
        ('Speaker 1', "Welcome to this week's episode of AI Insights, where we explore the latest developments in the field of artificial intelligence. So, let's get started!"),
        ('Speaker 2', "Sounds exciting!  Can you give me a brief overview?"),
        ('Speaker 1', "Thank you for joining me on this episode of AI Insights! If you want to learn more about knowledge distillation and its applications, be sure to check out our resources section, where we've curated a list of papers, articles, and tutorials to help you get started."),
        ('Speaker 2', "And if you're interested in building your own AI model using knowledge distillation, maybe we can even do a follow-up episode on how to get started... Umm, let's discuss that further next time."),
    ]
    """
    '''
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

def tts_server(text, speaker_description):
    url = 'http://localhost:8000/v1/audio/speech'

    payload = {
        'input': text,
        'voice' : speaker_description
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
    
   
if __name__ == "__main__":
    main()

