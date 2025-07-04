from pathlib import Path
from openai import OpenAI
import platform
import subprocess

# Initialize OpenAI client
openai = OpenAI(base_url="https://dwani-whisper.hf.space/v1", api_key="cant-be-empty")
model_id = "speaches-ai/Kokoro-82M-v1.0-ONNX"
voice_id = "af_heart"

# Create speech
res = openai.audio.speech.create(
    model=model_id,
    voice=voice_id,
    input="Hello, world!, i am sachin",
    response_format="wav",
    speed=1,
)

# Save the audio to a file
output_file = Path("output.wav")
with output_file.open("wb") as f:
    f.write(res.response.read())

# Autoplay the audio based on the operating system
def play_audio(file_path):
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["start", str(file_path)], shell=True)
        elif system == "Darwin":  # macOS
            subprocess.run(["afplay", str(file_path)])
        elif system == "Linux":
            subprocess.run(["aplay", str(file_path)])
        else:
            print(f"Autoplay not supported on {system}. Please open {file_path} manually.")
    except Exception as e:
        print(f"Error playing audio: {e}")

play_audio(output_file)