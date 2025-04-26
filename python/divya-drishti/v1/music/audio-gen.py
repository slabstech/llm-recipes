import torchaudio
from audiocraft.models import AudioGen
import soundfile as sf
import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:64"

def generate_sound(description):
    # Load the pretrained AudioGen model
    model = AudioGen.get_pretrained('facebook/audiogen-medium')
    model.set_generation_params(
        use_sampling=True,
        top_k=50,
        duration=5
    )

    # Generate audio (returns a tensor of shape [batch_size, channels, samples])
    wav = model.generate([description])  # Pass description as a list to ensure batch processing

    # Move to CPU and convert to NumPy
    audio_cpu = wav[0].cpu()  # Take the first sample (batch_size=1)
    audio_numpy = audio_cpu.numpy()

    # Ensure correct shape
    if audio_numpy.ndim == 3:  # Shape: [1, channels, samples]
        audio_numpy = audio_numpy[0]  # Remove batch dimension
    if audio_numpy.ndim == 2:  # Shape: [channels, samples]
        # Transpose to [samples, channels] as required by soundfile
        audio_numpy = audio_numpy.T
    elif audio_numpy.ndim == 1:  # Mono audio
        # Reshape to [samples, 1] for soundfile
        audio_numpy = audio_numpy[:, None]

    # Verify the shape
    print(f"Audio shape: {audio_numpy.shape}")

    # Write to file using the model's sample rate
    sf.write('audio.wav', audio_numpy, model.sample_rate)

def main():
    generate_sound("dog barks")

if __name__ == "__main__":
    main()