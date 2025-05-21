# main.py
import io
import tempfile
import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
import soundfile as sf
import torchaudio
from time import time
from contextlib import asynccontextmanager
from typing import List
from logging_config import logger

# Import extracted modules
from config.settings import parse_arguments
from config.constants import SUPPORTED_LANGUAGES, LANGUAGE_TO_SCRIPT, QUANTIZATION_CONFIG
from utils.audio_utils import load_audio_from_url as load_audio_from_url_original
from utils.tts_utils import load_audio_from_url, synthesize_speech, SynthesizeRequest, KannadaSynthesizeRequest, EXAMPLES
from models.schemas import (
    ChatRequest, ChatResponse, TranslationRequest, TranslationResponse,
    TranscriptionResponse
)
from core.managers import registry, initialize_managers
from routes.chat import router as chat_router
from routes.translate import router as translate_router
from routes.speech import router as speech_router
from routes.health import router as health_router

# Parse arguments early
args = parse_arguments()

# Lifespan Event Handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    def load_all_models():
        try:
            # Load LLM model
            # Load TTS model
            logger.info("Loading TTS model...")
            registry.tts_manager.load()
            logger.info("TTS model loaded successfully")

            logger.info("All models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            raise

    logger.info("Initializing managers...")
    initialize_managers(args.config, args)
    logger.info("Starting sequential model loading...")
    load_all_models()
    yield
    registry.llm_manager.unload()
    logger.info("Server shutdown complete")

# FastAPI App
app = FastAPI(
    title="Dhwani API",
    description="AI Chat API supporting Indian languages",
    version="1.0.0",
    redirect_slashes=False,
    lifespan=lifespan
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Timing Middleware
@app.middleware("http")
async def add_request_timing(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    end_time = time()
    duration = end_time - start_time
    logger.info(f"Request to {request.url.path} took {duration:.3f} seconds")
    response.headers["X-Response-Time"] = f"{duration:.3f}"
    return response

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Mount Routers
app.include_router(chat_router)
app.include_router(translate_router)
app.include_router(speech_router)
app.include_router(health_router)

# Main Execution
if __name__ == "__main__":
    host = args.host
    port = args.port
    uvicorn.run(app, host=host, port=port)