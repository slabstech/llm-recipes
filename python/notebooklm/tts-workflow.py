from transformers import BarkModel, AutoProcessor, AutoTokenizer
import torch
import json
import numpy as np
from parler_tts import ParlerTTSForConditionalGeneration
from tqdm import tqdm


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

    # Play audio in notebook
    ipd.Audio(audio_arr, rate=model.config.sampling_rate)


def generate_speaker1_audio(text):
    """Generate audio using ParlerTTS for Speaker 1"""
    input_ids = parler_tokenizer(speaker1_description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = parler_tokenizer(text, return_tensors="pt").input_ids.to(device)
    generation = parler_model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()
    return audio_arr, parler_model.config.sampling_rate


def generate_speaker2_audio(text):
    """Generate audio using Bark for Speaker 2"""
    inputs = bark_processor(text, voice_preset="v2/en_speaker_6").to(device)
    speech_output = bark_model.generate(**inputs, temperature=0.9, semantic_temperature=0.8)
    audio_arr = speech_output[0].cpu().numpy()
    return audio_arr, bark_sampling_rate

test_parler_audio()