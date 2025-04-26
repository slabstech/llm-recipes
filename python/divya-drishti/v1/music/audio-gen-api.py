import torchaudio
from audiocraft.models import AudioGen
import soundfile as sf
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Set CUDA memory configuration
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:64"

# Initialize FastAPI app
app = FastAPI(title="Audio Generation API")

# Define request model
class AudioRequest(BaseModel):
    prompt: str
    seconds: float = 5.0  # Default to 5 seconds

# Initialize AudioGen model globally to avoid reloading on each request
model = None

@app.on_event("startup")
def load_model():
    global model
    try:
        model = AudioGen.get_pretrained('facebook/audiogen-medium')
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise HTTPException(status_code=500, detail="Failed to load AudioGen model")

def generate_audio(prompt: str, duration: float) -> str:
    """
    Generate audio based on the given prompt and duration.
    Returns the path to the generated audio file.
    """
    try:
        # Set generation parameters
        model.set_generation_params(
            use_sampling=True,
            top_k=50,
            duration=duration
        )

        # Generate audio (returns a tensor of shape [batch_size, channels, samples])
        wav = model.generate([prompt])  # Pass prompt as a list

        # Move to CPU and convert to NumPy
        audio_cpu = wav[0].cpu()  # Take the first sample (batch_size=1)
        audio_numpy = audio_cpu.numpy()

        # Ensure correct shape
        if audio_numpy.ndim == 3:  # Shape: [1, channels, samples]
            audio_numpy = audio_numpy[0]  # Remove batch dimension
        if audio_numpy.ndim == 2:  # Shape: [channels, samples]
            # Transpose to [samples, channels] as required by soundfile
            audio_numpy = audio_numpy.T
        elif audio_numpy.ndim == 1:  # Mono audio
            # Reshape to [samples, 1] for soundfile
            audio_numpy = audio_numpy[:, None]

        # Define output file path
        output_file = "audio.wav"

        # Write to file using the model's sample rate
        sf.write(output_file, audio_numpy, model.sample_rate)

        return output_file

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating audio: {str(e)}")

@app.post("/generate-audio/")
async def generate_audio_endpoint(request: AudioRequest):
    """
    Endpoint to generate audio from a prompt and duration.
    Returns the path to the generated audio file.
    """
    if request.seconds <= 0:
        raise HTTPException(status_code=400, detail="Duration must be greater than 0")
    
    try:
        output_file = generate_audio(request.prompt, request.seconds)
        return {"message": "Audio generated successfully", "file_path": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=7861)