import base64
from PIL import Image
from io import BytesIO
import ollama

image = Image.open("../../docs/speech-inference.png")

buffered = BytesIO()
image.save(buffered, format="JPEG")
img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

base64_image = f"data:image/jpeg;base64,{img_str}"

response = ollama.chat(
    model="llava",
    messages=[
        {
            "role": "user",
            "content": "What is in this image?",
            "images": [base64_image]
        }
    ]
)
