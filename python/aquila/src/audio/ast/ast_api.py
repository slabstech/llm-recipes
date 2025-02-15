import time
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from transformers import ASTFeatureExtractor, ASTForAudioClassification
import torch
import soundfile as sf
import io
import numpy as np
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import requests
import base64
import json
import os

app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

# Load the model and feature extractor
model_name = "MIT/ast-finetuned-audioset-10-10-0.4593"
feature_extractor = ASTFeatureExtractor.from_pretrained(model_name)
model = ASTForAudioClassification.from_pretrained(model_name)
label2id = model.config.label2id
id2label = {v: k for k, v in label2id.items()}

def chunk_audio(audio, sr, chunk_size):
    """Splits the audio into chunks of chunk_size seconds."""
    chunk_length = chunk_size * sr
    num_chunks = int(np.ceil(len(audio) / chunk_length))
    chunks = [audio[i*chunk_length:(i+1)*chunk_length] for i in range(num_chunks)]
    return chunks

@app.post("/predict_audio")
async def predict_audio(file: UploadFile = File(...)):
    start_time = time.time()  # Record the start time
    try:
        # Read the audio file
        audio_bytes = await file.read()
        audio, sr = sf.read(io.BytesIO(audio_bytes))

        # Split the audio into 5-second chunks
        chunk_size = 5  # 5 seconds
        chunks = chunk_audio(audio, sr, chunk_size)

        # Preprocess the audio chunks
        inputs = [feature_extractor(chunk, sampling_rate=sr, return_tensors="pt") for chunk in chunks]

        # Perform batch inference
        model.eval()
        predictions = []
        with torch.no_grad():
            for i, input_data in enumerate(inputs):
                outputs = model(**input_data)
                logits = outputs.logits
                predicted_class_id = torch.argmax(logits, dim=-1).item()
                predicted_label = id2label[predicted_class_id]
                start_timestamp = i * chunk_size
                end_timestamp = min((i + 1) * chunk_size, len(audio) / sr)
                predictions.append({
                    "start_time": start_timestamp,
                    "end_time": end_timestamp,
                    "predicted_class": predicted_label
                })

        elapsed_time = time.time() - start_time  # Calculate elapsed time
        return JSONResponse(content={"filename": file.filename, "predictions": predictions, "time_taken(ms)": elapsed_time})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def explain_image(image_bytes, model, prompt, ollama_url):
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
    url = ollama_url + "/api/chat"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [encoded_image]
            }
        ]
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    response_data = ""
    if response.status_code == 200:
        for chunk in response.iter_lines():
            if chunk:
                data = chunk.decode('utf-8')
                data_list = json.loads(data)
                content = data_list['message']['content']
                response_data += content
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
    return response_data

@app.post("/predict_image")
async def predict_image(file: UploadFile = File(...)):
    try:
        # Read the image file
        image_bytes = await file.read()

        # Define the model, prompt, and URL
        model = "minicpm-v"
        prompt = "explain this image?"
        url = "http://localhost:11434"

        # Get the image explanation
        image_metadata = explain_image(image_bytes, model, prompt, url)

        return JSONResponse(content={"filename": file.filename, "metadata": image_metadata})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)