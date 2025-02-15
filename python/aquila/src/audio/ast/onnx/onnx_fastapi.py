from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from transformers import ASTFeatureExtractor
import onnxruntime
import soundfile as sf
import io
import time
import traceback

app = FastAPI()

# Load the feature extractor
model_name = "MIT/ast-finetuned-audioset-10-10-0.4593"
feature_extractor = ASTFeatureExtractor.from_pretrained(model_name)

# Load the ONNX model
onnx_model_path = "ast_model.onnx"
ort_session = onnxruntime.InferenceSession(onnx_model_path)

def load_label_mappings(file_path):
    label2id = {}
    id2label = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            parts = line.split(',')
            if len(parts) != 2:
                continue  # Skip lines that do not have exactly two parts
            label = parts[0].strip('"')
            try:
                idx = int(parts[1])
            except ValueError:
                continue  # Skip lines where the index cannot be converted to an integer
            label2id[label] = idx
            id2label[idx] = label
    return label2id, id2label

label2id, id2label = load_label_mappings('labels.txt')

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        start_time = time.time()

        # Read the audio file
        audio_bytes = await file.read()
        audio, sr = sf.read(io.BytesIO(audio_bytes))

        # Preprocess the audio
        inputs = feature_extractor(audio, sampling_rate=sr, return_tensors="pt")

        # Convert inputs to ONNX format
        ort_inputs = {ort_session.get_inputs()[0].name: inputs["input_values"].numpy()}

        # Perform inference
        ort_outs = ort_session.run(None, ort_inputs)
        logits = ort_outs[0]
        predicted_class_id = logits.argmax(axis=-1).item()
        predicted_label = id2label[predicted_class_id]

        end_time = time.time()
        processing_time = end_time - start_time

        print(f"Processed {file.filename} in {processing_time:.2f} seconds")

        return JSONResponse(content={
            "filename": file.filename,
            "predicted_class": predicted_label,
            "processing_time": processing_time
        })
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)