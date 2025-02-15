from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from transformers import ASTFeatureExtractor, ASTForAudioClassification
import torch
import librosa
import io

app = FastAPI()

# Load the model and feature extractor
model_name = "MIT/ast-finetuned-audioset-10-10-0.4593"
feature_extractor = ASTFeatureExtractor.from_pretrained(model_name)
model = ASTForAudioClassification.from_pretrained(model_name)
label2id = model.config.label2id
id2label = {v: k for k, v in label2id.items()}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read the audio file
        audio_bytes = await file.read()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=feature_extractor.sampling_rate)

        # Preprocess the audio
        inputs = feature_extractor(audio, sampling_rate=sr, return_tensors="pt")

        # Perform inference
        model.eval()
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            predicted_class_id = torch.argmax(logits, dim=-1).item()
            predicted_label = id2label[predicted_class_id]

        return JSONResponse(content={"filename": file.filename, "predicted_class": predicted_label})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)