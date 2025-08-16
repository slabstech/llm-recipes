import cv2


def take_picture(filename):
    # Initialize the webcam (0 is usually the default camera)
    cam = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cam.isOpened():
        print("Cannot open camera")
        exit()

    # Read one frame from the camera
    ret, frame = cam.read()

    # If a frame is successfully returned, save it as an image
    if ret:
        cv2.imwrite(filename, frame)
        print(f"Photo captured and saved as  {filename}")
    
    else:
        print("Failed to capture image")

    # Release the camera
    cam.release()

    return ret

from io import BytesIO

from openai import OpenAI
import base64

def get_openai_client(model: str) -> OpenAI:
    """Initialize OpenAI client with model-specific base URL."""
    valid_models = ["gemma3", "moondream", "qwen2.5vl", "qwen3", "sarvam-m", "deepseek-r1"]
    if model not in valid_models:
        raise ValueError(f"Invalid model: {model}. Choose from: {', '.join(valid_models)}")
    
    model_ports = {
        "qwen3": "9100",
        "gemma3": "9000",
        "moondream": "7882",
        "qwen2.5vl": "7883",
        "sarvam-m": "7884",
        "deepseek-r1": "7885"
    }
    base_url = f"http://0.0.0.0:{model_ports[model]}/v1"

    return OpenAI(api_key="http", base_url=base_url)

def encode_image(image: BytesIO) -> str:
    """Encode image bytes to base64 string."""
    return base64.b64encode(image.read()).decode("utf-8")

def ocr_page_with_rolm(img_base64: str, model: str) -> str:
    """Perform OCR on the provided base64 image using the specified model."""
    try:
        client = get_openai_client(model)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{img_base64}"}
                        },
                        {"type": "text", "text": "Return the plain text extracted from this image."}
                    ]
                }
            ],
            temperature=0.2,
            max_tokens=4096
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")
    

def describe_image(filename):
    image_bytes = await file.read()
    image = BytesIO(image_bytes)
    img_base64 = encode_image(image)
    text = ocr_page_with_rolm(img_base64, model="gemma3")


filename = "photo.jpg"
take_picture(filename=filename)


describe_image(filename)