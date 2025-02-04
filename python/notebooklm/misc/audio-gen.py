import torchaudio
from audiocraft.models import AudioGen
from audiocraft.data.audio import audio_write
import time

import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:64"

def generate_sound(description):
    model = AudioGen.get_pretrained('facebook/audiogen-medium')
    model.set_generation_params(duration=3)  # generate 5 seconds.
    wav = model.generate(description)  # generates 3 samples.
    audio_write(f'abc', wav.cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
    
'''
descriptions = ['dog barking', 'sirene of an emergency vehicle', 'footsteps in a corridor']
wav = model.generate(descriptions)  # generates 3 samples.

for idx, one_wav in enumerate(wav):
    # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
    audio_write(f'{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
    time.sleep(1)
'''
def main():
    generate_sound("dog barks")

if __name__ == "__main__":
    main()

