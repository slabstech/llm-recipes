import torch
from transformers import ASTFeatureExtractor, ASTForAudioClassification

# Load the model and feature extractor
model_name = "MIT/ast-finetuned-audioset-10-10-0.4593"
feature_extractor = ASTFeatureExtractor.from_pretrained(model_name)
model = ASTForAudioClassification.from_pretrained(model_name)

# Prepare dummy input for export
# Assuming the model expects a 1D waveform input of length 16000 samples
dummy_input = torch.randn(1, 16000)  # Adjust the shape according to your model's input requirements
dummy_input = feature_extractor(dummy_input, sampling_rate=16000, return_tensors="pt")

# Export the model to ONNX format
onnx_model_path = "ast_model.onnx"
torch.onnx.export(
    model,
    (dummy_input["input_values"],),
    onnx_model_path,
    export_params=True,
    opset_version=14,
    do_constant_folding=True,
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}}
)