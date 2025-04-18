from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import torch
import base64
import json
from io import BytesIO
from PIL import Image
from transformers import AutoProcessor, Qwen2VLForConditionalGeneration
from olmocr.data.renderpdf import render_pdf_to_base64png
from olmocr.prompts import build_finetuning_prompt
from olmocr.prompts.anchor import get_anchor_text
import tempfile
import os

# Initialize FastAPI app
app = FastAPI(
    title="PDF OCR API",
    description="API for extracting text from PDF pages using olmOCR",
    version="1.0.0"
)

# Initialize the model and processor
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "allenai/olmOCR-7B-0225-preview", torch_dtype=torch.bfloat16
).eval()
processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

@app.post("/extract-text/")
async def extract_text_from_pdf(file: UploadFile = File(...), page_number: int = 1):
    """
    Extract text from a specific page of a PDF file.

    Args:
        file (UploadFile): The PDF file to process.
        page_number (int): The page number to extract text from (1-based indexing).

    Returns:
        JSONResponse: The extracted page content (natural_text) or error details.
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

        # Build the prompt using document metadata
        try:
            anchor_text = get_anchor_text(
                temp_file_path, page_number, pdf_engine="pdfreport", target_length=4000
            )
            prompt = build_finetuning_prompt(anchor_text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to build prompt: {str(e)}")

        # Build the full prompt
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
                ],
            }
        ]

        # Apply the chat template and processor
        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        main_image = Image.open(BytesIO(base64.b64decode(image_base64)))

        inputs = processor(
            text=[text],
            images=[main_image],
            padding=True,
            return_tensors="pt",
        )
        inputs = {key: value.to(device) for (key, value) in inputs.items()}

        # Generate the output
        try:
            output = model.generate(
                **inputs,
                temperature=0.8,
                max_new_tokens=1024,  # Increased to capture full content
                num_return_sequences=1,
                do_sample=True,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model inference failed: {str(e)}")

        # Decode the output
        prompt_length = inputs["input_ids"].shape[1]
        new_tokens = output[:, prompt_length:]
        text_output = processor.tokenizer.batch_decode(new_tokens, skip_special_tokens=True)

        # Clean up temporary file
        os.remove(temp_file_path)

        # Parse the natural_text from the output
        try:
            output_dict = json.loads(text_output[0])
            page_content = output_dict.get("natural_text", "")
            return JSONResponse(content={"page_content": page_content})
        except json.JSONDecodeError:
            return JSONResponse(
                content={"error": "Failed to parse output as JSON", "raw_output": text_output[0]},
                status_code=500
            )

    except Exception as e:
        # Clean up in case of error
        if 'temp_file_path' in locals():
            try:
                os.remove(temp_file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
async def root():
    """
    Root endpoint for health check.
    """
    return {"message": "PDF OCR API is running"}