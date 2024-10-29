import gradio as gr
from spiritlm.model.spiritlm_model import Spiritlm, OutputModality, GenerationInput, ContentType
from transformers import GenerationConfig
import torchaudio
import torch
import tempfile
import os
import numpy as np

# Initialize the Spirit LM model with the modified class
spirit_lm = Spiritlm("spirit-lm-base-7b")

def generate_output(input_type, input_content_text, input_content_audio, output_modality, temperature, top_p, max_new_tokens, do_sample, speaker_id):
    generation_config = GenerationConfig(
        temperature=temperature,
        top_p=top_p,
        max_new_tokens=max_new_tokens,
        do_sample=do_sample,
    )

    if input_type == "text":
        interleaved_inputs = [GenerationInput(content=input_content_text, content_type=ContentType.TEXT)]
    elif input_type == "audio":
        # Load audio file
        waveform, sample_rate = torchaudio.load(input_content_audio)
        interleaved_inputs = [GenerationInput(content=waveform.squeeze(0), content_type=ContentType.SPEECH)]
    else:
        raise ValueError("Invalid input type")

    outputs = spirit_lm.generate(
        interleaved_inputs=interleaved_inputs,
        output_modality=OutputModality[output_modality.upper()],
        generation_config=generation_config,
        speaker_id=speaker_id,  # Pass the selected speaker ID
    )

    text_output = ""
    audio_output = None

    for output in outputs:
        if output.content_type == ContentType.TEXT:
            text_output = output.content
        elif output.content_type == ContentType.SPEECH:
            # Ensure output.content is a NumPy array
            if isinstance(output.content, np.ndarray):
                # Debugging: Print shape and dtype of the audio data
                print("Audio data shape:", output.content.shape)
                print("Audio data dtype:", output.content.dtype)

                # Ensure the audio data is in the correct format
                if len(output.content.shape) == 1:
                    # Mono audio data
                    audio_data = torch.from_numpy(output.content).unsqueeze(0)
                else:
                    # Stereo audio data
                    audio_data = torch.from_numpy(output.content)

                # Save the audio content to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
                    torchaudio.save(temp_audio_file.name, audio_data, 16000)
                    audio_output = temp_audio_file.name
            else:
                raise TypeError("Expected output.content to be a NumPy array, but got {}".format(type(output.content)))

    return text_output, audio_output

# Define the Gradio interface
iface = gr.Interface(
    fn=generate_output,
    inputs=[
        gr.Radio(["text", "audio"], label="Input Type", value="text"),
        gr.Textbox(label="Input Content (Text)"),
        gr.Audio(label="Input Content (Audio)", type="filepath"),
        gr.Radio(["TEXT", "SPEECH", "ARBITRARY"], label="Output Modality", value="SPEECH"),
        gr.Slider(0, 1, step=0.1, value=0.9, label="Temperature"),
        gr.Slider(0, 1, step=0.05, value=0.95, label="Top P"),
        gr.Slider(1, 800, step=1, value=500, label="Max New Tokens"),
        gr.Checkbox(value=True, label="Do Sample"),
        gr.Dropdown(choices=[0, 1, 2, 3], value=0, label="Speaker ID"), 
    ],
    outputs=[gr.Textbox(label="Generated Text"), gr.Audio(label="Generated Audio")],
    title="Spirit LM WebUI Demo",
    description="Demo for generating text or audio using the Spirit LM model.",
    flagging_mode="never",
)

# Launch the interface
iface.launch()