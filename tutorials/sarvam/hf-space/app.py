from transformers import AutoTokenizer, AutoModelForCausalLM, TextGenerationPipeline
import gradio as gr

# Load the model and tokenizer
model = AutoModelForCausalLM.from_pretrained("sarvamai/sarvam-1")
tokenizer = AutoTokenizer.from_pretrained("sarvamai/sarvam-1")
tokenizer.pad_token_id = tokenizer.eos_token_id

# Create the text generation pipeline
pipe = TextGenerationPipeline(model=model, tokenizer=tokenizer, device="cuda", torch_dtype="bfloat16", return_full_text=False)

# Define prediction function
def generate_text(prompt):
    return pipe(prompt)[0]['generated_text']

# Set up Gradio interface
demo = gr.Interface(
    fn=generate_text,
    inputs=gr.Textbox(label="Enter your prompt"),
    outputs=gr.Textbox(label="Generated text"),
    title="Text Generation with Sarvam-1",
    description="Enter a prompt to generate text using the Sarvam-1 model."
)

# Launch the demo
demo.launch(share=True)
