from openai import OpenAI
import base64

# Function to encode an image to base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Configure the OpenAI client to use vLLM's API server
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# Get the first available model (assuming it supports vision)
models = client.models.list()
model = models.data[0].id

# Target language for translation
tgt_lang = "Kannada"

# Path to the local image file (replace with your actual image path)
image_path = "sample_image.jpg"  # Example: replace with "/path/to/your/image.jpg"

# Encode the image to base64
try:
    base64_image = encode_image_to_base64(image_path)
    image_content = f"data:image/jpeg;base64,{base64_image}"
except FileNotFoundError:
    print(f"Error: Image file '{image_path}' not found.")
    exit(1)

# Define the prompt for extracting and translating text from the image
messages = [
    {
        "role": "system",
        "content": f"You are an assistant that extracts text from images and translates it into {tgt_lang}. Extract all visible text from the provided image and translate it into {tgt_lang}. If no text is found, return 'No text found in the image.'"
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": f"Extract the text from the image and translate it into {tgt_lang}."},
            {"type": "image_url", "image_url": {"url": image_content}}
        ]
    }
]

# Make the API call to extract and translate text
try:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.01
    )
    output_text = response.choices[0].message.content
except Exception as e:
    print(f"Error during API call: {str(e)}")
    output_text = "Failed to process the image."

# Print the input and output
print("Input Image:", image_path)
print(f"Translated Text (to {tgt_lang}):", output_text)
