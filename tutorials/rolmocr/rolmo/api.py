from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI
import base64
import json
from io import BytesIO
from PIL import Image
import tempfile
import os
from olmocr.data.renderpdf import render_pdf_to_base64png
from olmocr.prompts import build_finetuning_prompt
from olmocr.prompts.anchor import get_anchor_text

# Initialize FastAPI app
app = FastAPI(
    title="Combined OCR API",
    description="API for extracting text from PDF pages and PNG images using RolmOCR",
    version="1.0.0"
)

# Initialize OpenAI client for RolmOCR
openai_client = OpenAI(api_key="123", base_url="http://localhost:8000/v1")
rolm_model = "reducto/RolmOCR"

def encode_image(image: BytesIO) -> str:
    """Encode image bytes to base64 string."""
    return base64.b64encode(image.read()).decode("utf-8")

def ocr_page_with_rolm(img_base64: str) -> str:
    """Perform OCR on the provided base64 image using RolmOCR via OpenAI API."""
    try:
        response = openai_client.chat.completions.create(
            model=rolm_model,
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
        raise HTTPException(status_code=500, detail=f"RolmOCR processing failed: {str(e)}")

@app.post("/extract-text/", response_model=dict)
async def extract_text_from_pdf(file: UploadFile = File(...), page_number: int = 1):
    """
    Extract text from a specific page of a PDF file using RolmOCR.

    Args:
        file (UploadFile): The PDF file to process.
        page_number (int): The page number to extract text from (1-based indexing).

    Returns:
        JSONResponse: The extracted page content or error details.
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")

        # Save the uploaded PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        # Render the specified page to an image
        try:
            image_base64 = render_pdf_to_base64png(
                temp_file_path, page_number, target_longest_image_dim=1024
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to render PDF page: {str(e)}")

        # Perform OCR using RolmOCR
        try:
            page_content = ocr_page_with_rolm(image_base64)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

        # Clean up temporary file
        os.remove(temp_file_path)

        return JSONResponse(content={"page_content": page_content})

    except Exception as e:
        # Clean up in case of error
        if 'temp_file_path' in locals():
            try:
                os.remove(temp_file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/ocr", response_model=dict)
async def ocr_image(file: UploadFile = File(...)):
    """
    Upload a PNG image and extract text using RolmOCR.

    Args:
        file (UploadFile): The PNG image to process.

    Returns:
        dict: The extracted text.
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
    return {"message": "Combined OCR API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)