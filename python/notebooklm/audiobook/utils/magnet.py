from audiocraft.models import MAGNeT
from audiocraft.data.audio import audio_write

model = MAGNeT.get_pretrained("facebook/audio-magnet-medium")

descriptions = ["""
                Wind whistles through the trees, leaves rustle quietly in the background. Birds chirp
sporadically""", """ then suddenly silence, as if something had startled them. """, """ A branch cracks in the
distance, the sound echoes through the clearing."""]

wav = model.generate(descriptions)  # generates 2 samples.

for idx, one_wav in enumerate(wav):
    # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
    audio_write(f'{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness")
