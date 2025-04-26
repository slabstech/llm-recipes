import time
from contextlib import asynccontextmanager
from typing import Annotated, Any, OrderedDict

import huggingface_hub
import torch
from fastapi import Body, FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from huggingface_hub.hf_api import ModelInfo
from openai.types import Model
from audiocraft.models import MAGNeT
from audiocraft.data.audio import audio_write

from magnet_server.config import SPEED, ResponseFormat, config
from magnet_server.logger import logger

# Check if GPU is available and set device accordingly
if torch.cuda.is_available():
    device = "cuda:0"
    logger.info("GPU will be used for inference")
else:
    device = "cpu"
    logger.info("CPU will be used for inference")
torch_dtype = torch.float16 if device != "cpu" else torch.float32

class ModelManager:
    def __init__(self):
        self.model: dict[str, MAGNeT] = {}

    def load_model(self, model_name: str) -> MAGNeT:
        logger.debug(f"Loading {model_name}...")
        start = time.perf_counter()
        model = MAGNeT.get_pretrained(model_name).to(device, dtype=torch_dtype)
        logger.info(f"Loaded {model_name} in {time.perf_counter() - start:.2f} seconds")
        return model

    def get_or_load_model(self, model_name: str) -> MAGNeT:
        if model_name not in self.model:
            logger.info(f"Model {model_name} isn't already loaded")
            if len(self.model) == config.max_models:
                logger.info("Unloading the oldest loaded model")
                del self.model[next(iter(self.model))]
            self.model[model_name] = self.load_model(model_name)
        return self.model[model_name]

model_manager = ModelManager()

@asynccontextmanager
async def lifespan(_: FastAPI):
    if not config.lazy_load_model:
        model_manager.get_or_load_model(config.model)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health() -> Response:
    return Response(status_code=200, content="OK")

@app.get("/v1/models", response_model=list[Model])
def get_models() -> list[Model]:
    models = list(huggingface_hub.list_models(model_name="audio-magnet"))
    models = [
        Model(
            id=model.id,
            created=int(model.created_at.timestamp()),
            object="model",
            owned_by=model.id.split("/")[0],
        )
        for model in models
        if model.created_at is not None
    ]
    return models

@app.get("/v1/models/{model_name:path}", response_model=Model)
def get_model(model_name: str) -> Model:
    models = list(huggingface_hub.list_models(model_name=model_name))
    if len(models) == 0:
        raise HTTPException(status_code=404, detail="Model doesn't exist")
    exact_match: ModelInfo | None = None
    for model in models:
        if model.id == model_name:
            exact_match = model
            break
    if exact_match is None:
        raise HTTPException(
            status_code=404,
            detail=f"Model doesn't exist. Possible matches: {', '.join([model.id for model in models])}",
        )
    assert exact_match.created_at is not None
    return Model(
        id=exact_match.id,
        created=int(exact_match.created_at.timestamp()),
        object="model",
        owned_by=exact_match.id.split("/")[0],
    )

# https://platform.openai.com/docs/api-reference/audio/createSpeech
@app.post("/v1/audio/speech")
async def generate_audio(
    input: Annotated[str, Body()],
    voice: Annotated[str, Body()] = config.voice,
    model: Annotated[str, Body()] = config.model,
    response_format: Annotated[ResponseFormat, Body()] = config.response_format,
    speed: Annotated[float, Body()] = SPEED,
) -> FileResponse:
    tts = model_manager.get_or_load_model(model)
    if speed != SPEED:
        logger.warning(
            "Specifying speed isn't supported by this model. Audio will be generated with the default speed"
        )
    start = time.perf_counter()
    descriptions = [input]  # Pass the input text as a list of descriptions
    wav = tts.generate(descriptions)  # Generates audio samples
    for idx, one_wav in enumerate(wav):
        audio_path = f"out.{response_format}"
        audio_write(audio_path, one_wav.cpu(), tts.sample_rate, strategy="loudness")
    logger.info(
        f"Took {time.perf_counter() - start:.2f} seconds to generate audio for {len(input.split())} words using {device.upper()}"
    )
    return FileResponse(audio_path, media_type=f"audio/{response_format}")