from transformers import MambaConfig, Mamba2ForCausalLM, AutoTokenizer
import torch
model_id = 'mistralai/Mamba-Codestral-7B-v0.1'
tokenizer = AutoTokenizer.from_pretrained(model_id, revision='refs/pr/9', from_slow=True, legacy=False)
model = Mamba2ForCausalLM.from_pretrained(model_id, revision='refs/pr/9')
input_ids = tokenizer("Hey how are you doing?", return_tensors= "pt")["input_ids"]

out = model.generate(input_ids, max_new_tokens=10)
print(tokenizer.batch_decode(out))
