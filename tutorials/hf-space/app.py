import spaces
import gradio as gr
from transformers import AutoTokenizer, Mamba2ForCausalLM

model_id = 'gaganyatri/codestral-7B'

# Load the Mamba model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id, from_slow=True, legacy=False)

model = Mamba2ForCausalLM.from_pretrained(model_id)

@spaces.GPU(duration=10)
# Define the chatbot function
def chat(input_text):
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    output = model.generate(input_ids, max_length=2500)
    return tokenizer.batch_decode(output)

# Create the Gradio interface
demo = gr.Interface(fn=chat, inputs="text", outputs="text")

# Launch the app
demo.launch(share=True)
