
import torch
import requests
import numpy as np

import io
# Device setup
if torch.cuda.is_available():
    device = "cuda:0"
    
else:
    device = "cpu"
torch_dtype = torch.bfloat16 if device != "cpu" else torch.float32

class TTSManager:
    def __init__(self, device_type=device):
        self.device_type = device_type
        self.model = None
        self.repo_id = "ai4bharat/IndicF5"

    def load(self):
        if not self.model:
            logger.info("Loading TTS model IndicF5...")
            self.model = AutoModel.from_pretrained(
                self.repo_id,
                trust_remote_code=True
            )
            self.model = self.model.to(self.device_type)
            logger.info("TTS model IndicF5 loaded")

    def synthesize(self, text, ref_audio_path, ref_text):
        if not self.model:
            raise ValueError("TTS model not loaded")
        return self.model(text, ref_audio_path=ref_audio_path, ref_text=ref_text)


import tempfile
import soundfile as sf
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings
import uvicorn
from fastapi import Depends, FastAPI, File, HTTPException, Query, Request, UploadFile, Body, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse
# TTS Constants
EXAMPLES = [
    {
        "audio_name": "KAN_F (Happy)",
        "audio_url": "https://github.com/AI4Bharat/IndicF5/raw/refs/heads/main/prompts/KAN_F_HAPPY_00001.wav",
        "ref_text": "ನಮ್‌ ಫ್ರಿಜ್ಜಲ್ಲಿ  ಕೂಲಿಂಗ್‌ ಸಮಸ್ಯೆ ಆಗಿ ನಾನ್‌ ಭಾಳ ದಿನದಿಂದ ಒದ್ದಾಡ್ತಿದ್ದೆ, ಆದ್ರೆ ಅದ್ನೀಗ ಮೆಕಾನಿಕ್ ಆಗಿರೋ ನಿಮ್‌ ಸಹಾಯ್ದಿಂದ ಬಗೆಹರಿಸ್ಕೋಬೋದು ಅಂತಾಗಿ ನಿರಾಳ ಆಯ್ತು ನಂಗೆ.",
        "synth_text": "ಚೆನ್ನೈನ ಶೇರ್ ಆಟೋ ಪ್ರಯಾಣಿಕರ ನಡುವೆ ಆಹಾರವನ್ನು ಹಂಚಿಕೊಂಡು ತಿನ್ನುವುದು ನನಗೆ ಮನಸ್ಸಿಗೆ ತುಂಬಾ ಒಳ್ಳೆಯದೆನಿಸುವ ವಿಷಯ."
    },
]

# Pydantic models for TTS
class SynthesizeRequest(BaseModel):
    text: str
    ref_audio_name: str
    ref_text: str = None

class KannadaSynthesizeRequest(BaseModel):
    text: str

# TTS Functions
def load_audio_from_url(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        audio_data, sample_rate = sf.read(io.BytesIO(response.content))
        return sample_rate, audio_data
    raise HTTPException(status_code=500, detail="Failed to load reference audio from URL.")

def synthesize_speech(tts_manager: TTSManager, text: str, ref_audio_name: str, ref_text: str):
    ref_audio_url = None
    for example in EXAMPLES:
        if example["audio_name"] == ref_audio_name:
            ref_audio_url = example["audio_url"]
            if not ref_text:
                ref_text = example["ref_text"]
            break
    
    if not ref_audio_url:
        raise HTTPException(status_code=400, detail="Invalid reference audio name.")
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text to synthesize cannot be empty.")
    if not ref_text or not ref_text.strip():
        raise HTTPException(status_code=400, detail="Reference text cannot be empty.")

    sample_rate, audio_data = load_audio_from_url(ref_audio_url)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        sf.write(temp_audio.name, audio_data, samplerate=sample_rate, format='WAV')
        temp_audio.flush()
        audio = tts_manager.synthesize(text, ref_audio_path=temp_audio.name, ref_text=ref_text)

    if audio.dtype == np.int16:
        audio = audio.astype(np.float32) / 32768.0
    buffer = io.BytesIO()
    sf.write(buffer, audio, 24000, format='WAV')
    buffer.seek(0)
    return buffer
