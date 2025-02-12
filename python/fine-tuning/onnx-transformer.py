import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import onnxruntime as ort
import numpy as np
import torch
import onnx


def convert_to_onnx():
    # Load the model and tokenizer
    device = "cuda:0"
    model_name =  "parler-tts/parler-tts-mini-v1.1"
    torch_dtype = torch.float16

    model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(  # type: ignore
        device,  # type: ignore
        dtype=torch_dtype,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    input = "hello_world"
    prompt_input_ids = tokenizer(input, return_tensors="pt").input_ids.to(device)

    # Cast input_ids to float tensors
    #prompt_input_ids = prompt_input_ids.float()
    example_input = {
        "input_ids": prompt_input_ids  # Adjust dimensions as needed
    }


    torch.onnx.export(
        model.text_encoder,  # Replace with text_encoder or decoder as needed
        (example_input["input_ids"],),  # Provide example input
        "parler_tts_text_encoder.onnx",  # Output ONNX file name
        export_params=True,
        opset_version=13,
        do_constant_folding=True,
        input_names=["input_ids"],
        output_names=["output"],
        dynamic_axes={"input_ids": {0: "batch_size"}, "output": {0: "batch_size"}}
    )


def run_onnx_model():

    onnx_model = onnx.load("parler_tts_text_encoder.onnx")
    onnx.checker.check_model(onnx_model)

    # Assuming tokenizer and device are already defined and loaded
    input = "hello_world"
    device = "cuda:0"
    model_name =  "parler-tts/parler-tts-mini-v1.1"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    prompt_input_ids = tokenizer(input, return_tensors="pt").input_ids.to(device)

    # Cast input_ids to float tensors if necessary
    #prompt_input_ids = prompt_input_ids.float()

    # Convert the tensor to numpy array for ONNX runtime
    onnx_input = prompt_input_ids.cpu().numpy().astype(np.int64)

    # Load the ONNX model
    ort_session = ort.InferenceSession("parler_tts_text_encoder.onnx")

    # Define the input name for the ONNX model
    input_name = ort_session.get_inputs()[0].name

    # Run inference
    onnx_output = ort_session.run(None, {input_name: onnx_input})

    # The output is a list of numpy arrays
    print(onnx_output)
    print('run onnx')


run_onnx_model()

