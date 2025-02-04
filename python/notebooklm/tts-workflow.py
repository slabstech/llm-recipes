from transformers import BarkModel, AutoProcessor, AutoTokenizer
import torch
import json
import numpy as np
from parler_tts import ParlerTTSForConditionalGeneration
from tqdm import tqdm
from IPython.display import Audio
import IPython.display as ipd
import soundfile as sf

device = "cuda" if torch.cuda.is_available() else "cpu"

speaker_1_description = """
        Laura's voice is expressive and dramatic in delivery, speaking at a moderately fast pace with a very close recording that almost has no background noise.
    """
speaker_2_description = """
        Michael's voice is deep and resonant, with a calm and authoritative tone. He speaks at a steady pace, ensuring clarity and precision in his delivery. The recording is clear with minimal background noise, providing a professional and engaging listening experience.
    """

def test_parler_audio():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load model and tokenizer
    model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler-tts-mini-v1").to(device)
    tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")

    # Define text and description
    text_prompt = """
    Exactly! And the distillation part is where you take a LARGE-model,and compress-it down into a smaller, more efficient model that can run on devices with limited resources.
    """
    description = """
    Laura's voice is expressive and dramatic in delivery, speaking at a fast pace with a very close recording that almost has no background noise.
    """
    # Tokenize inputs
    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(text_prompt, return_tensors="pt").input_ids.to(device)

    # Generate audio
    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()

# Save audio to file
    output_file = "output_audio.wav"
    sf.write(output_file, audio_arr, model.config.sampling_rate)

    # Play audio in notebook
    ipd.Audio(audio_arr, rate=model.config.sampling_rate)


def generate_speaker_audio(text, speaker_description):
    """Generate audio using ParlerTTS for Speaker 1"""
    input_ids = parler_tokenizer(speaker_description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = parler_tokenizer(text, return_tensors="pt").input_ids.to(device)
    generation = parler_model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()
    return audio_arr, parler_model.config.sampling_rate



def numpy_to_audio_segment(audio_arr, sampling_rate):
    """Convert numpy array to AudioSegment"""
    # Convert to 16-bit PCM
    audio_int16 = (audio_arr * 32767).astype(np.int16)
    
    # Create WAV file in memory
    byte_io = io.BytesIO()
    wavfile.write(byte_io, sampling_rate, audio_int16)
    byte_io.seek(0)
    
    # Convert to AudioSegment
    return AudioSegment.from_wav(byte_io)



def generate_podcast():
    final_audio = None

    for speaker, text in tqdm(ast.literal_eval(PODCAST_TEXT), desc="Generating podcast segments", unit="segment"):
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


def main():
    speaker_1_description = """
        Laura's voice is expressive and dramatic in delivery, speaking at a moderately fast pace with a very close recording that almost has no background noise.
    """
