from huggingface_hub import snapshot_download
from pathlib import Path

mistral_models_path = Path.home().joinpath('mistral_models', '7B-Instruct-v0.3')
mistral_models_path.mkdir(parents=True, exist_ok=True)

#snapshot_download(repo_id="mistralai/Mistral-7B-Instruct-v0.3", allow_patterns=["params.json", "consolidated.safetensors", "tokenizer.model.v3"], local_dir=mistral_models_path)
snapshot_download(repo_id="SrikanthChellappa/Mistral-7B-Instruct-v0.3-AWQ-4Bit", allow_patterns=["params.json", "model.safetensors", "tokenizer.model"], local_dir=mistral_models_path)