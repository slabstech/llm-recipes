from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from vllm import LLM, SamplingParams
import uvicorn
import json
import time

# Initialize FastAPI app
app = FastAPI(title="OpenAI-Compatible Chat Completions API with vLLM")

# Configuration for vLLM
VLLM_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Replace with your model

# Initialize vLLM client
try:
    llm = LLM(model=VLLM_MODEL)  # Removed api_endpoint
except Exception as e:
    print(f"Failed to initialize vLLM client: {e}")
    raise

# Define request models compatible with OpenAI API
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 512
    top_p: Optional[float] = 1.0
    stream: Optional[bool] = False

class ChatCompletionChoice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Dict[str, int]

# Helper function to convert messages to vLLM prompt
def messages_to_prompt(messages: List[Message]) -> str:
    prompt = ""
    for msg in messages:
        role = msg.role
        content = msg.content
        if role == "system":
            prompt += f"[System]: {content}\n"
        elif role == "user":
            prompt += f"[User]: {content}\n"
        elif role == "assistant":
            prompt += f"[Assistant]: {content}\n"
    prompt += "[Assistant]: "
    return prompt

# Chat completions endpoint
@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    if request.stream:
        raise HTTPException(status_code=501, detail="Streaming not supported yet")

    # Convert OpenAI-style messages to vLLM prompt
    prompt = messages_to_prompt(request.messages)

    # Set vLLM sampling parameters
    sampling_params = SamplingParams(
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p
    )

    try:
        # Generate response using vLLM
        outputs = llm.generate([prompt], sampling_params=sampling_params)
        generated_text = outputs[0].outputs[0].text.strip()

        # Construct OpenAI-compatible response
        response = ChatCompletionResponse(
            id=f"chatcmpl-{hash(prompt)}",
            created=int(time.time()),
            model=request.model,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=Message(role="assistant", content=generated_text),
                    finish_reason="stop"
                )
            ],
            usage={
                "prompt_tokens": len(prompt.split()),  # Approximate token count
                "completion_tokens": len(generated_text.split()),  # Approximate
                "total_tokens": len(prompt.split()) + len(generated_text.split())
            }
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"vLLM error: {str(e)}")

# Run the FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)