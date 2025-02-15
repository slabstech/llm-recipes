from transformers import ASTFeatureExtractor, ASTForAudioClassification
import torch
import librosa
import os

model_name = "MIT/ast-finetuned-audioset-10-10-0.4593"
feature_extractor = ASTFeatureExtractor.from_pretrained(model_name)
model = ASTForAudioClassification.from_pretrained(model_name)

# Load and preprocess audio files
def load_audio_files(directory, feature_extractor, sr, max_files=10):
    audio_files = [f for f in os.listdir(directory) if f.endswith('.wav')][:max_files]
    audio_features = []
    filenames = []
    for file in audio_files:
        audio, sr = librosa.load(os.path.join(directory, file), sr=sr)
        inputs = feature_extractor(audio, sampling_rate=sr, return_tensors="pt")
        audio_features.append(inputs)
        filenames.append(file)
    return audio_features, filenames

# Directory containing the audio files
base_directory = "../data/sorted_audio/"
subdirectories = [os.path.join(base_directory, d) for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]

# Batch size for inference
batch_size = 3

# Process each subdirectory
all_results = []
all_filenames = []
model.eval()
with torch.no_grad():
    for subdir in subdirectories:
        audio_features, filenames = load_audio_files(subdir, feature_extractor, feature_extractor.sampling_rate)
        results = []
        for i in range(0, len(audio_features), batch_size):
            batch = {key: torch.cat([feature[key] for feature in audio_features[i:i+batch_size]]) for key in audio_features[0].keys()}
            outputs = model(**batch)
            logits = outputs.logits
            predicted_classes = torch.argmax(logits, dim=-1).tolist()
            results.extend(predicted_classes)
        all_results.extend(results)
        all_filenames.extend(filenames)

# Convert predicted class IDs to labels
label2id = model.config.label2id
id2label = {v: k for k, v in label2id.items()}
predicted_labels = [id2label[cls] for cls in all_results]

# Print results
for filename, label in zip(all_filenames, predicted_labels):
    print(f"File {filename}: Predicted class: {label}")