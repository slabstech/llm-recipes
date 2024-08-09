from transformers import MambaConfig, Mamba2ForCausalLM, AutoTokenizer
import torch

# Replace these paths with the actual paths to the model and tokenizer files
model_config_path = 'config.json'
tokenizer_vocab_path = 'tokenizer.json'

model_config = MambaConfig.from_json_file(model_config_path)
model = Mamba2ForCausalLM(model_config).cuda()

# Load the model weights from the Safetensors files
safetensors_paths = ['model-00001-of-00003.safetensors', 'model-00002-of-00003.safetensors', 'model-00003-of-00003.safetensors']

model_state_dict = {}
for path in safetensors_paths:
    state_dict = torch.load(path, map_location=torch.device('cuda'))
    model_state_dict.update(state_dict)
model.load_state_dict(model_state_dict)
model.eval()

tokenizer = AutoTokenizer.from_pretrained(tokenizer_vocab_path, from_slow=True, legacy=False)

input_ids = tokenizer("Hey how are you doing?", return_tensors= "pt")["input_ids"]
