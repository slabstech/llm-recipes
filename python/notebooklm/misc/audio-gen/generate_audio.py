import torch
from stable_audio_tools.audio_to_audio import AudioToAudio
from stable_audio_tools.utils import save_audio

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = AudioToAudio.from_pretrained(
    'checkpoints/stable-audio-1_0-base.pth',
    device=device
)

#prompt = "Post-Rock, Guitars, Drum Kit, Bass, Strings, Euphoric, Up-Lifting, Moody, Flowing, Raw, Epic, Sentimental, 125 BPM"

prompt = "dog barking, door closes with a creek, footsteps heard from a distance, 125 BPM"


audio = model.generate(
    prompt,
    duration=30,
    seed=42,
    guidance_scale=3,
    num_inference_steps=50
)

save_audio(audio, '/output/generated_audio.wav', sample_rate=44100)
print("Audio saved as /output/generated_audio.wav")
