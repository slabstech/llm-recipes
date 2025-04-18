from fastapi import FastAPI, File, UploadFile, HTTPException
from openai import OpenAI
import base64
from io import BytesIO

app = FastAPI(title="RolmOCR API")

# Initialize OpenAI client
client = OpenAI(api_key="123", base_url="http://localhost:8000/v1")
model = "reducto/RolmOCR-7b"

def encode_image(image: BytesIO) -> str:
    """Encode image bytes to base64 string."""
    return base64.b64encode(image.read()).decode("utf-8")

def ocr_page_with_rolm(img_base64: str) -> str:
    """Perform OCR on the provided base64 image using RolmOCR."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{img_base64}"},
                        },
                        {
                            "type": "text",
                            "text": "Return the plain text representation of this document as if you were reading it naturally.\n",
                        },
                    ],
                }
            ],
            temperature=0.2,
            max_tokens=4096
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

@app.post("/ocr", response_model=dict)
async def ocr_image(file: UploadFile = File(...)):
    """
    Upload an image and extract text using RolmOCR.
    Accepts PNG images and returns the extracted text.
    """
    # Validate file type
    if not file.content_type.startswith("image/png"):
        raise HTTPException(status_code=400, detail="Only PNG images are supported")

    try:
        # Read image file
        image_bytes = await file.read()
        image = BytesIO(image_bytes)
        
        # Encode to base64
        img_base64 = encode_image(image)
        
        # Perform OCR
        text = ocr_page_with_rolm(img_base64)
        
        return {"extracted_text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"message": "RolmOCR API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)