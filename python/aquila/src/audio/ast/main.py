from transformers import ASTFeatureExtractor, ASTForAudioClassification
import torch
import librosa

model_name = "MIT/ast-finetuned-audioset-10-10-0.4593"
feature_extractor = ASTFeatureExtractor.from_pretrained(model_name)
model = ASTForAudioClassification.from_pretrained(model_name)


# 0 - vehicle
# 1 - shooting
audio, sr = librosa.load("1.wav", sr=feature_extractor.sampling_rate)

inputs = feature_extractor(audio, sampling_rate=sr, return_tensors="pt")


with torch.no_grad():
    outputs = model(**inputs)

logits = outputs.logits
predicted_class = torch.argmax(logits, dim=-1).item()

label2id = model.config.label2id
id2label = {v: k for k, v in label2id.items()}
predicted_label = id2label[predicted_class]
print(f"Predicted class: {predicted_label}")
