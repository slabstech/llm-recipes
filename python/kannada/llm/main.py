from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llama_cpp import Llama
from sse_starlette.sse import EventSourceResponse
import os

MODEL_PATH = "/models/krutrim-2-instruct-Q4_K_M.gguf"

# Input schemas
class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 128
    temperature: float = 0.7
    top_p: float = 0.9

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    max_tokens: int = 256
    temperature: float = 0.7

# Model lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    
    app.state.llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_gpu_layers=-1 if os.getenv("GPU_ENABLED") else 0,
        chat_format="llama-2"
    )
    yield
    del app.state.llm

# Initialize FastAPI
app = FastAPI(lifespan=lifespan)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection
def get_llm():
    return app.state.llm

# API Endpoints
@app.post("/v1/completions")
async def create_completion(
    request: CompletionRequest,
    llm: Llama = Depends(get_llm)
):
    try:
        response = llm.create_completion(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/chat/completions")
async def create_chat_completion(
    request: ChatRequest,
    llm: Llama = Depends(get_llm)
):
    try:
        messages = [m.dict() for m in request.messages]
        response = llm.create_chat_completion(
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/chat/completions/stream")
async def stream_chat_completion(
    request: ChatRequest,
    llm: Llama = Depends(get_llm)
):
    async def event_generator():
        messages = [m.dict() for m in request.messages]
        stream = llm.create_chat_completion(
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            stream=True
        )
        
        for chunk in stream:
            yield {
                "data": chunk,
                "event": "message"
            }
        yield {"event": "end"}

    return EventSourceResponse(event_generator())

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
