# core/managers.py
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoProcessor, AutoModel, Gemma3ForConditionalGeneration, BitsAndBytesConfig
from logging_config import logger
from config.settings import Settings
from config.constants import SUPPORTED_LANGUAGES
from utils.device_utils import setup_device
from utils.time_utils import time_to_words
from fastapi import HTTPException
from PIL import Image
from typing import List, Dict, Any
import torch
from PIL import Image
from typing import List, Dict, Any
#import logging
import os
import time
from contextlib import nullcontext

#logger = logging.getLogger(__name__)
import torch
from PIL import Image
from typing import List, Dict, Any
import logging
import os
import time
from contextlib import nullcontext
import asyncio
import hashlib


def resize_image(image: Image.Image, max_size: int = 512) -> Image.Image:
    """Resize image to ensure consistent dimensions while preserving aspect ratio."""
    start_time = time.time()
    image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    logger.debug(f"Resized image to max_size={max_size} in {time.time() - start_time:.3f}s")
    return image

def get_image_hash(image: Image.Image) -> str:
    """Generate a hash for an image to enable caching."""
    image_bytes = image.convert("RGB").tobytes()
    return hashlib.md5(image_bytes).hexdigest()


# Device setup
device, torch_dtype = setup_device()

# Initialize settings
settings = Settings()

# Manager Registry
class ManagerRegistry:
    def __init__(self):
        self.llm_manager = None
        self.tts_manager = None

# Singleton registry instance
registry = ManagerRegistry()

enable_quantization = os.getenv("ENABLE_QUANTIZATION", "false").lower() == "true"
                
# Set quantization config based on environment variable
quantization_config = None
if enable_quantization:
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    logger.info("Quantization enabled via environment variable")
else:
    logger.info("Quantization disabled")



# Updated TTS Manager
class TTSManager:
    def __init__(self, device_type=device):
        self.device_type = device_type
        self.model = None
        self.repo_id = "ai4bharat/IndicF5"

    def load(self):
        if not self.model:
            logger.info("Loading TTS model IndicF5...")
            try:
                self.model = AutoModel.from_pretrained(
                    self.repo_id,
                    trust_remote_code=True
                )
                self.model = self.model.to(self.device_type)
                logger.info("TTS model IndicF5 loaded")
            except Exception as e:
                logger.error(f"Failed to load TTS model: {str(e)}")
                raise

    def synthesize(self, text, ref_audio_path, ref_text):
        if not self.model:
            raise ValueError("TTS model not loaded")
        return self.model(text, ref_audio_path=ref_audio_path, ref_text=ref_text)


def initialize_managers(config_name: str, args):
    from config.settings import load_config
    config_data = load_config()
    if config_name not in config_data["configs"]:
        raise ValueError(f"Invalid config: {config_name}. Available: {list(config_data['configs'].keys())}")
    
    selected_config = config_data["configs"][config_name]
    global_settings = config_data["global_settings"]

    settings.llm_model_name = selected_config["components"]["LLM"]["model"]
    settings.max_tokens = selected_config["components"]["LLM"]["max_tokens"]
    settings.host = global_settings["host"]
    settings.port = global_settings["port"]
    settings.chat_rate_limit = global_settings["chat_rate_limit"]
    settings.speech_rate_limit = global_settings["speech_rate_limit"]

    #registry.llm_manager = LLMManager(settings.llm_model_name)
    #registry.model_manager = ModelManager()
    #registry.asr_manager = ASRModelManager()
    registry.tts_manager = TTSManager()

    