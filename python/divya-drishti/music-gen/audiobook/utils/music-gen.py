from audiocraft.models import MusicGen
from audiocraft.models import MultiBandDiffusion

import soundfile as sf

# Using small model, better results would be obtained with `medium` or `large`.
model = MusicGen.get_pretrained('facebook/musicgen-small')


model.set_generation_params(
    use_sampling=True,
    top_k=250,
    duration=5
)

output = model.generate(
    descriptions=[
        #'80s pop track with bassy drums and synth',
        #'90s rock song with loud guitars and heavy drums',
        #'Progressive rock drum and bass solo',
        #'Punk Rock song with loud drum and power guitar',
        #'Bluesy guitar instrumental with soulful licks and a driving rhythm section',
        #'Jazz Funk song with slap bass and powerful saxophone',
        'drum and bass beat with intense percussions'
    ],
    progress=True, return_tokens=True
)

audio_cpu = output[0].cpu()
audio_numpy = audio_cpu.numpy()
if audio_numpy.ndim > 2:
    # Flatten extra dimensions
    audio_numpy = audio_numpy.squeeze()
sf.write('generated_audio.wav', audio_numpy, 32000)

