import ollama

def process_text_chunk(text_chunk, SYS_PROMPT,  chunk_num):
    
    """Process a chunk of text and return both input and output for verification"""
    conversation = [
        {"role": "system", "content": SYS_PROMPT},
        {"role": "user", "content": text_chunk},
    ]

    # Prepare the prompt
    #prompt = ollama.apply_chat_template(conversation)

    response = ollama.chat(model='qwen2.5:latest', messages=conversation)
    #print(response['message']['content'])

    '''
        # Generate the response using Ollama
        response = ollama.generate(
            prompt,
            temperature=0.7,
            top_p=0.9,
            max_new_tokens=512
        )
    
    processed_text = response['choices'][0]['text'].strip()
    '''
    processed_text = response['message']['content']
    # Print chunk information for monitoring
    #print(f"\n{'='*40} Chunk {chunk_num} {'='*40}")
    print(f"INPUT TEXT:\n{text_chunk[:500]}...")  # Show first 500 chars of input
    print(f"\nPROCESSED TEXT:\n{processed_text[:500]}...")  # Show first 500 chars of output
    print(f"{'='*90}\n")

    return processed_text
