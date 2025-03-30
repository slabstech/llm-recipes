import gradio as gr
import requests

# API endpoint
API_URL = "https://slabstech-image-gen-edit-stability.hf.space/edit-image/"

def edit_image(image_path, instruction, steps, text_cfg_scale, image_cfg_scale, seed):
    # Open the uploaded image file in binary mode
    with open(image_path, "rb") as f:
        files = {
            "file": ("original.jpg", f, "image/jpeg")
        }
        # Prepare the payload for the POST request
        data = {
            "instruction": instruction,
            "steps": steps,
            "text_cfg_scale": text_cfg_scale,
            "image_cfg_scale": image_cfg_scale,
            "seed": seed
        }

        # Send the POST request to the API
        headers = {
            "accept": "application/json"
        }
        response = requests.post(API_URL, files=files, data=data, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Assuming the API returns the edited image as binary data
            return response.content  # Return the image binary data
        else:
            return f"Error: {response.status_code} - {response.text}"

# Create Gradio interface
with gr.Blocks(title="Image Edit API Interface") as demo:
    gr.Markdown("# Image Editing with Stability API")
    gr.Markdown("Upload an image and customize the editing parameters.")
    
    with gr.Row():
        with gr.Column():
            # Input components
            image_input = gr.Image(type="filepath", label="Upload Image")  # Changed to "filepath"
            instruction_input = gr.Textbox(
                value="check the surrounding and camouflage based on the environment",
                label="Instruction"
            )
            steps_input = gr.Slider(1, 200, value=100, step=1, label="Steps")
            text_cfg_scale_input = gr.Slider(1.0, 10.0, value=7.5, step=0.1, label="Text CFG Scale")
            image_cfg_scale_input = gr.Slider(1.0, 10.0, value=1.5, step=0.1, label="Image CFG Scale")
            seed_input = gr.Number(value=1371, label="Seed")
            submit_btn = gr.Button("Edit Image")
        
        with gr.Column():
            # Output component
            output_image = gr.Image(label="Edited Image")
    
    # Connect the inputs to the function and output
    submit_btn.click(
        fn=edit_image,
        inputs=[image_input, instruction_input, steps_input, text_cfg_scale_input, image_cfg_scale_input, seed_input],
        outputs=output_image
    )

# Launch the interface
demo.launch()