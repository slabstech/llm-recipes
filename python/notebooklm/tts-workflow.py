import json
import numpy as np
from tqdm import tqdm
from IPython.display import Audio
import IPython.display as ipd
import soundfile as sf
import io
from scipy.io import wavfile
from pydub import AudioSegment
import requests


speaker_1_description = """
        Laura's voice is expressive and dramatic in delivery, speaking at a moderately fast pace with a very close recording that almost has no background noise.
    """
speaker_2_description = """
        Michael's voice is deep and resonant, with a calm and authoritative tone. He speaks at a steady pace, ensuring clarity and precision in his delivery. The recording is clear with minimal background noise, providing a professional and engaging listening experience.
    """



def generate_podcast(podcast_text):
    final_audio = None

    for speaker, text in tqdm(ast.literal_eval(podcast_text), desc="Generating podcast segments", unit="segment"):
        if speaker == "Speaker 1":
            audio_arr, rate = generate_speaker_audio(text, speaker_1_description)
        else:  # Speaker 2
            audio_arr, rate = generate_speaker_audio(text, speaker_2_description)
        
        # Convert to AudioSegment (pydub will handle sample rate conversion automatically)
        audio_segment = numpy_to_audio_segment(audio_arr, rate)
        
        # Add to final audio
        if final_audio is None:
            final_audio = audio_segment
        else:
            final_audio += audio_segment

    final_audio.export("_podcast.mp3", 
                  format="mp3", 
                  bitrate="192k",
                  parameters=["-q:a", "0"])

import ast

def main():
    speaker_1_description = """
        Laura's voice is expressive and dramatic in delivery, speaking at a moderately fast pace with a very close recording that almost has no background noise.
    """

    podcast_ast = """
    [
        ('Speaker 1', "Welcome to this week's episode of AI Insights, where we explore the latest developments in the field of artificial intelligence. Today, we're going to dive into the fascinating world of knowledge distillation, a methodology that transfers advanced capabilities from leading proprietary Large Language Models, or LLMs, to their open-source counterparts. Joining me on this journey is my co-host, who's new to the topic, and I'll be guiding them through the ins and outs of knowledge distillation. So, let's get started!"),
        ('Speaker 2', "Sounds exciting! I've heard of knowledge distillation, but I'm not entirely sure what it's all about. Can you give me a brief overview?"),
        ('Speaker 1', "Of course! Knowledge distillation is a technique that enables the transfer of knowledge from a large, complex model, like GPT-4 or Gemini, to a smaller, more efficient model, like LLaMA or Mistral. This process allows the smaller model to learn from the teacher model's output, enabling it to acquire similar capabilities. Think of it like a master chef teaching their apprentice the art of cooking – the apprentice doesn't need to start from scratch."),
        ('Speaker 2', "Hmm, that sounds interesting. So, it's like a teacher-student relationship, where the teacher model guides the student model to learn from its output... Umm, can you explain this process in more detail?"),
        ('Speaker 1', "Thank you for joining me on this episode of AI Insights! If you want to learn more about knowledge distillation and its applications, be sure to check out our resources section, where we've curated a list of papers, articles, and tutorials to help you get started."),
        ('Speaker 2', "And if you're interested in building your own AI model using knowledge distillation, maybe we can even do a follow-up episode on how to get started... Umm, let's discuss that further next time."),
    ]
"""

    podcast_ast_short = """
    [
        ('Speaker 1', "Welcome to this week's episode of AI Insights, where we explore the latest developments in the field of artificial intelligence. Today, we're going to dive into the fascinating world of knowledge distillation, a methodology that transfers advanced capabilities from leading proprietary Large Language Models, or LLMs, to their open-source counterparts. Joining me on this journey is my co-host, who's new to the topic, and I'll be guiding them through the ins and outs of knowledge distillation. So, let's get started!"),
    ]
"""

    tts_server("hello world")
    #test_parler_audio()

def tts_server(text):
    url = 'http://localhost:8000/v1/audio/speech'

    payload = {
        'input': text
    }

    # Make the POST request
    response = requests.post(url, json=payload)
    # Check if the request was successful
    if response.status_code == 200:
        # Save the audio response as a WAV file
        # Create a file-like object with the audio data
        with open('audio.mp3', 'wb') as f:
            f.write(response.content)
        '''
        byte_io = io.BytesIO(response.content)
        audio_int16 = (audio_arr * 32767).astype(np.int16)
        rate = 44100
        wavfile.write(byte_io, rate, )
        byte_io.seek(0)
    
        # Convert to AudioSegment
        final_audio = AudioSegment.from_wav(byte_io)
    
        final_audio.export("_podcast.mp3", 
                format="mp3", 
                bitrate="192k",
                parameters=["-q:a", "0"])
        '''

   
if __name__ == "__main__":
    main()

