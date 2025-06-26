from huggingface_hub import snapshot_download
import os

model_dir = "gemma-3n-E2B-it-ONNX/"

files_to_download = [
    "onnx/embed_tokens_quantized.onnx",    "onnx/embed_tokens_quantized.onnx_data",
    "onnx/audio_encoder.onnx",
    "onnx/vision_encoder.onnx",    "onnx/vision_encoder.onnx_data",
    "onnx/decoder_model_merged_q4.onnx"
]

snapshot_download(
    repo_id="onnx-community/gemma-3n-E2B-it-ONNX",
    repo_type="model",
    local_dir=model_dir,
    allow_patterns=files_to_download  # <-- use allow_patterns, not include
)

embed_model_path   = os.path.join(model_dir, "onnx/embed_tokens_quantized.onnx")
audio_model_path   = os.path.join(model_dir, "onnx/audio_encoder.onnx")
vision_model_path  = os.path.join(model_dir, "onnx/vision_encoder.onnx")
decoder_model_path = os.path.join(model_dir, "onnx/decoder_model_merged_q4.onnx")
