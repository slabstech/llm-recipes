from PIL import Image
import base64
import io
from ollama import Client
def image_to_base64(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Create a BytesIO object to hold the image data
        buffered = io.BytesIO()
        # Save the image to the BytesIO object in a specific format (e.g., PNG)
        img.save(buffered, format="PNG")
        # Get the byte data from the BytesIO object
        img_bytes = buffered.getvalue()
        # Encode the byte data to base64
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        return img_base64


def test_code():
    image_path = '/home/gaganyatri/Downloads/books-rec-1.jpeg'  # Replace with your image path
    base64_image = image_to_base64(image_path)
    client = Client(host='http://localhost:21434')
    response = client.chat(
    model="x/llama3.2-vision:latest",
    messages=[{
    "role": "user",
    "content": "Describe this image?",
    "images": [base64_image]
    }],
)

    # Extract the model's response about the image
    cleaned_text = response['message']['content'].strip()
    print(f"Model Response: {cleaned_text}")
    # Example usage

test_code()
