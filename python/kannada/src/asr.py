import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor, WhisperTokenizer, WhisperFeatureExtractor
import soundfile as sf
import torchaudio


model = "ARTPARK-IISc/whisper-medium-vaani-kannada"
#model = "ARTPARK-IISc/whisper-small-vaani-kannada"

# Load tokenizer and feature extractor individually
feature_extractor = WhisperFeatureExtractor.from_pretrained(model)
#tokenizer = WhisperTokenizer.from_pretrained("openai/whisper-medium", language="Kannada", task="transcribe")
tokenizer = WhisperTokenizer.from_pretrained("openai/whisper-medium", language="Kannada", task="translate")
# Create the processor manually
processor = WhisperProcessor(feature_extractor=feature_extractor, tokenizer=tokenizer)

# Load and preprocess the audio file
audio_file_path = "../data/kannada_2.wav"  # replace with your audio file path

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the processor and model
model = WhisperForConditionalGeneration.from_pretrained(model).to(device)

# load audio
audio_data, sample_rate = sf.read(audio_file_path)

# Ensure the audio is 16kHz (Whisper expects 16kHz audio)
if sample_rate != 16000:
    # Convert audio data to float32
    audio_data = audio_data.astype('float32')
    resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
    audio_data = resampler(torch.tensor(audio_data).unsqueeze(0)).squeeze().numpy()

# Use the processor to prepare the input features
input_features = processor(audio_data, sampling_rate=16000, return_tensors="pt").input_features.to(device)

# Generate transcription (disable gradient calculation during inference)
with torch.no_grad():
    predicted_ids = model.generate(input_features)

# Decode the generated IDs into human-readable text
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

print(transcription)