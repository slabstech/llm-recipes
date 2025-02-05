import PyPDF2
from typing import Optional
import os
import requests
from tqdm.notebook import tqdm
import warnings

from utils.utils import process_text_chunk

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
    
    return extracted_text


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
        
def process_extracted_text(file_name, SYS_PROMPT):
    INPUT_FILE = file_name  # Replace with your file path
    CHUNK_SIZE = 1000  # Adjust chunk size if needed
    

    with open(INPUT_FILE, 'r', encoding='utf-8') as file:
        text = file.read()

    # Calculate number of chunks
    num_chunks = (len(text) + CHUNK_SIZE - 1) // CHUNK_SIZE
    print(num_chunks)

    # Cell 6: Process the file with ordered output
    # Create output file name
    output_file = f"clean_{os.path.basename(INPUT_FILE)}"

    chunks = create_word_bounded_chunks(text, CHUNK_SIZE)
    num_chunks = len(chunks)
    print(num_chunks)
    processed_text =process_chunks_to_output(output_file=output_file, chunks=chunks, SYS_PROMPT=SYS_PROMPT)

    print(f"\nProcessing complete!")
    print(f"Input file: {INPUT_FILE}")
    print(f"Output file: {output_file}")
    print(f"Total chunks processed: {num_chunks}")
    return processed_text


def main():

    # URL of the PDF file to download
    pdf_web_url = 'https://slabstech.com/assets/pdf/onwards.pdf'
    # Local filename to save the downloaded PDF
    local_filename = 'onwards.pdf'

    # Download the PDF file
    #download_online_pdf(pdf_web_url, local_filename)

    #parser_data(pdf_path=local_filename) 
    extracted_file_name = "extracted_text.txt"
    SYS_PROMPT = get_prompt_for_analysis()
    #process_extracted_text(extracted_file_name, SYS_PROMPT)
    
    # Preview the beginning and end of the complete processed text

    show_preview_output()
    
def show_preview_output():
    INPUT_FILE = "clean_extracted_text.txt"  # Replace with your file path

    with open(INPUT_FILE, 'r', encoding='utf-8') as file:
        text = file.read()
    print("\nPreview of final processed text:")
    print("\nBEGINNING:")
    print(text[:1000])
    print("\n...\n\nEND:")
    print(text[-1000:])


def process_chunks_to_output(output_file,chunks ,SYS_PROMPT):
    processed_text = ''

    with open(output_file, 'w', encoding='utf-8') as out_file:
        for chunk_num, chunk in enumerate(tqdm(chunks, desc="Processing chunks")):
            # Process chunk and append to complete text
            processed_chunk = process_text_chunk(chunk, SYS_PROMPT,  chunk_num)
            processed_text += processed_chunk + "\n"
            
            # Write chunk immediately to file
            out_file.write(processed_chunk + "\n")
            out_file.flush()
    
def get_prompt_for_analysis():

    SYS_PROMPT = """
    You are a world class text pre-processor, here is the raw data from a PDF, please parse and return it in a way that is crispy and usable to send to a podcast writer.

    The raw data is messed up with new lines, Latex math and you will see fluff that we can remove completely. Basically take away any details that you think might be useless in a podcast author's transcript.

    Remember, the podcast could be on any topic whatsoever so the issues listed above are not exhaustive

    Please be smart with what you remove and be creative ok?

    Remember DO NOT START SUMMARIZING THIS, YOU ARE ONLY CLEANING UP THE TEXT AND RE-WRITING WHEN NEEDED

    Be very smart and aggressive with removing details, you will get a running portion of the text and keep returning the processed text.

    PLEASE DO NOT ADD MARKDOWN FORMATTING, STOP ADDING SPECIAL CHARACTERS THAT MARKDOWN CAPATILISATION ETC LIKES

    ALWAYS start your response directly with processed text and NO ACKNOWLEDGEMENTS about my questions ok?
    Here is the text:
    """
    return SYS_PROMPT

def create_word_bounded_chunks(text, target_chunk_size):
    """
    Split text into chunks at word boundaries close to the target chunk size.
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        word_length = len(word) + 1  # +1 for the space
        if current_length + word_length > target_chunk_size and current_chunk:
            # Join the current chunk and add it to chunks
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length
    
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks



if __name__ == "__main__":
    main()
