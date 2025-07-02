import gradio as gr
import logging
import dwani
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure dwani API settings
dwani.api_key = os.getenv("DWANI_API_KEY")
dwani.api_base = os.getenv("DWANI_API_BASE_URL")

def process_pdf(pdf_file):
    logger.debug("Received inputs - PDF: %s",
                 pdf_file)

    # Validate inputs
    if not pdf_file:
        logger.error("No PDF file provided")
        return "Error: Please upload a PDF file", None

    # Get file path from Gradio File object
    file_path = pdf_file.name if hasattr(pdf_file, 'name') else pdf_file
    pages = set()
    pages.add(1)
    src_lang_code = "eng_Latn"
    tgt_lang_code = "kan_Knda"
    logger.debug("Calling API with file: %s, pages: %s, src_lang: %s, tgt_lang: %s",
                 file_path, pages, src_lang_code, tgt_lang_code)

    results = {}
    for page_number in pages:
        try:
            result = dwani.Documents.run_extract(
                file_path=file_path,
                page_number=page_number,
                src_lang=src_lang_code,
                tgt_lang=tgt_lang_code
            )
            logger.debug("API response for page %d: %s", page_number, result)

            # New response format: result contains 'pages' list
            page_data = None
            for p in result.get('pages', []):
                if p.get('processed_page') == page_number:
                    page_data = p
                    break

            if page_data is None:
                results[f"Page {page_number}"] = {"error": "No data returned for this page"}
                continue

            results[f"Page {page_number}"] = {
                "Original Text": page_data.get("page_content", "N/A"),
                "Response": ""
            }
        except dwani.exceptions.DwaniAPIError as e:
            logger.error("Dhwani API error on page %d: %s", page_number, str(e))
            results[f"Page {page_number}"] = {"error": f"API error: {str(e)}"}
        except Exception as e:
            logger.error("Unexpected error on page %d: %s", page_number, str(e))
            results[f"Page {page_number}"] = {"error": f"Unexpected error: {str(e)}"}

    return extract_contact_details(results), extract_education_details(results)


def extract_contact_details(extracted_resume):
    resume_str = str(extracted_resume)
    chat_prompt = resume_str+ " return only contact details from the resume "
    chat_response = dwani.Chat.direct(prompt=chat_prompt, model="gemma3")
    print(chat_response)
    return chat_response


def extract_education_details(extracted_resume):
    resume_str = str(extracted_resume)
    chat_prompt = resume_str + " return only education details from the resume "
    chat_response = dwani.Chat.direct(prompt=chat_prompt, model="gemma3")
    print(chat_response)
    return chat_response

# Define Gradio interface
with gr.Blocks(title="Resume Translator") as resume_translator:
    gr.Markdown("# Resume upload")
    gr.Markdown("Upload a Resume.")
    
    with gr.Row():
        with gr.Column():
            pdf_input = gr.File(label="Upload Resume", file_types=[".pdf"])

            submit_btn = gr.Button("Process")
        
        with gr.Column():
            output = gr.JSON(label="Response")
    
    submit_btn.click(
        fn=process_pdf,
        inputs=[pdf_input],
        outputs=output
    )



if __name__ == "__main__":
    resume_translator.launch()