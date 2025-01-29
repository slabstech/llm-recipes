import PyPDF2
from typing import Optional
import os
import torch
from accelerate import Accelerator
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests

from tqdm.notebook import tqdm
import warnings

warnings.filterwarnings('ignore')

def validate_pdf(file_path: str) -> bool:
    if not os.path.exists(file_path):
        print(f"Error: File not found at path: {file_path}")
        return False
    if not file_path.lower().endswith('.pdf'):
        print("Error: File is not a PDF")
        return False
    return True

def extract_text_from_pdf(file_path: str, max_chars: int = 100000) -> Optional[str]:
    if not validate_pdf(file_path):
        return None
    
    try:
        with open(file_path, 'rb') as file:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Get total number of pages
            num_pages = len(pdf_reader.pages)
            print(f"Processing PDF with {num_pages} pages...")
            
            extracted_text = []
            total_chars = 0
            
            # Iterate through all pages
            for page_num in range(num_pages):
                # Extract text from page
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # Check if adding this page's text would exceed the limit
                if total_chars + len(text) > max_chars:
                    # Only add text up to the limit
                    remaining_chars = max_chars - total_chars
                    extracted_text.append(text[:remaining_chars])
                    print(f"Reached {max_chars} character limit at page {page_num + 1}")
                    break
                
                extracted_text.append(text)
                total_chars += len(text)
                print(f"Processed page {page_num + 1}/{num_pages}")
            
            final_text = '\n'.join(extracted_text)
            print(f"\nExtraction complete! Total characters: {len(final_text)}")
            return final_text
            
    except PyPDF2.PdfReadError:
        print("Error: Invalid or corrupted PDF file")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None

# Get PDF metadata
def get_pdf_metadata(file_path: str) -> Optional[dict]:
    if not validate_pdf(file_path):
        return None
    
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            metadata = {
                'num_pages': len(pdf_reader.pages),
                'metadata': pdf_reader.metadata
            }
            return metadata
    except Exception as e:
        print(f"Error extracting metadata: {str(e)}")
        return None

def parser_data(pdf_path):
    # Extract metadata first
    print("Extracting metadata...")
    metadata = get_pdf_metadata(pdf_path)
    if metadata:
        print("\nPDF Metadata:")
        print(f"Number of pages: {metadata['num_pages']}")
        print("Document info:")
        for key, value in metadata['metadata'].items():
            print(f"{key}: {value}")

    # Extract text
    print("\nExtracting text...")
    extracted_text = extract_text_from_pdf(pdf_path)

    # Display first 500 characters of extracted text as preview
    if extracted_text:
        print("\nPreview of extracted text (first 500 characters):")
        print("-" * 50)
        print(extracted_text[:500])
        print("-" * 50)
        print(f"\nTotal characters extracted: {len(extracted_text)}")

    # Optional: Save the extracted text to a file
    if extracted_text:
        output_file = 'extracted_text.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        print(f"\nExtracted text has been saved to {output_file}")


def download_online_pdf(url, local_filename):

    if os.path.exists(local_filename):
        print(f'{local_filename} already exists. Skipping download.')
        return

    # Send a GET request to the URL
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Open a file in write-binary mode
        with open(local_filename, 'wb') as file:
            # Iterate over the response data in chunks
            for chunk in response.iter_content(chunk_size=8192):
                # Write each chunk to the file
                file.write(chunk)
        print(f'Downloaded {local_filename} successfully.')
    else:
        print(f'Failed to download file. Status code: {response.status_code}')
        

def main():

    # URL of the PDF file to download
    pdf_web_url = 'https://slabstech.com/assets/pdf/onwards.pdf'
    # Local filename to save the downloaded PDF
    local_filename = 'onwards.pdf'

    # Download the PDF file
    download_online_pdf(pdf_web_url, local_filename)

    parser_data(pdf_path=local_filename) 
    

if __name__ == "__main__":
    main()
