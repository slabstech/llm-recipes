import ollama

# Define the prompt template
prompt_template = "<|User|>{user_input}<|Assistant|>"

# User input
user_input = "What is 1+1?"

# Format the prompt
formatted_prompt = prompt_template.format(user_input=user_input)

# Make a request to the Ollama API
response = ollama.chat(model='hf.co/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF:Q4_K_M', messages=[
    {
        'role': 'user',
        'content': formatted_prompt
    }
])

# Print the response
print(response['message']['content'])
