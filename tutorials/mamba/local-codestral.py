from transformers import MambaConfig, Mamba2ForCausalLM, AutoTokenizer
import torch
# Replace these paths with the actual paths to the model and tokenizer files
model_config_path = 'config.json'
tokenizer_vocab_path = 'tokenizer.json'

model_config = MambaConfig.from_json_file(model_config_path)
model = Mamba2ForCausalLM(model_config)

# Load the model weights from the Safetensors files
model_state_dict = torch.load('model-00001-of-00003.safetensors', map_location=torch.device('cuda'))
model_state_dict2 = torch.load('model-00001-of-00003.safetensors', map_location=torch.device('cuda'))
model_state_dict3 = torch.load('model-00001-of-00003.safetensors', map_location=torch.device('cuda'))

model.load_state_dict(model_state_dict)
model.load_state_dict(model_state_dict2)
model.load_state_dict(model_state_dict3)

model.eval()

tokenizer = AutoTokenizer.from_pretrained(tokenizer_vocab_path, from_slow=True, legacy=False)

input_ids = tokenizer("Hey how are you doing?", return_tensors= "pt")["input_ids"]
