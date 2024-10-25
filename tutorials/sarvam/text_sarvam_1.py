from transformers import AutoTokenizer, AutoModelForCausalLM, TextGenerationPipeline

# initialize a HF pipeline for easy use
model = AutoModelForCausalLM.from_pretrained("sarvamai/sarvam-1")
tokenizer = AutoTokenizer.from_pretrained("sarvamai/sarvam-1")
tokenizer.pad_token_id = tokenizer.eos_token_id
pipe = TextGenerationPipeline(model=model, tokenizer=tokenizer, device="cuda", torch_dtype="bfloat16", return_full_text=False)



###

gen_kwargs = {
  "temperature": 0.01, # we are introducing a small amount of stocasticity in the model generation process
  "repetition_penalty": 1.2, # discourage the model from repeating recently generated tokens
  "max_new_tokens": 256, # maximum number of tokens to generate
  "stop_strings": ["</s>", "\n\n"], # if these tokens are seen, stop the generation
  "tokenizer": tokenizer, # tokenizer of the model
} # works best with these defaults



### 
# a simple wrapper to get text completions
def gen(prompt):
  # having a trailing space hurts the model generation; let us strip them
  prompt = prompt.rstrip()
  output = pipe(prompt, **gen_kwargs)
  print(output[0]["generated_text"])

###
gen("Here is a simple sorting algorithm implemented in Python:")

###
prompt = """*ಬೆಂಗಳೂರಿನ ಇತಿಹಾಸ*

ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ ಬೆಂಗಳೂರು ಇವತ್ತು"""

gen(prompt)

#####
prompt = """English: The main motive of the Manhattan Project was to develop a nuclear bomb
Oriya: ମ୍ୟାନହାଟନ ପ୍ରକଳ୍ପର ମୁଖ୍ୟ ଉଦ୍ଦେଶ୍ୟ ଥିଲା ପରମାଣୁ ବୋମା ବିକଶିତ କରିବା

English: It was done during World War II and was a major factor during the last stages of the war.
Oriya: ଏହା ଦ୍ବିତୀୟ ବିଶ୍ୱଯୁଦ୍ଧ ସମୟରେ କରାଯାଇଥିଲା ଏବଂ ଯୁଦ୍ଧର ଶେଷ ପର୍ଯ୍ୟାୟରେ ଏହା ଏକ ପ୍ରମୁଖ କାରଣ ଥିଲା।

English: The current population of earth is about to exceed 8 billion, but experts say that this is not a cause for alarm.
Oriya: ପୃଥିବୀର ବର୍ତ୍ତମାନର ଜନସଂଖ୍ୟା ୮ ବିଲିୟନରୁ ଅଧିକ, କିନ୍ତୁ ବିଶେଷଜ୍ଞମାନେ କହୁଛନ୍ତି ଯେ ଏହା ଚିନ୍ତାର କାରଣ ନୁହେଁ।

English: The first horcrux that Harry Potter destroyed was Tom Riddle's diary.
Oriya:"""

gen(prompt)


######
prompt = """देश और उनकी राजधानियाँ:
चीन -> बीजिंग
भारत -> नई दिल्ली
यूएस -> वाशिंगटन डीसी
केन्या ->"""

gen(prompt)
####
'''
!pip install peft datasets
'''


import datasets
import transformers
from peft import (
    LoraConfig,
    PeftModel,
    get_peft_model,
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    HfArgumentParser,
    TrainingArguments,
    Trainer,
    default_data_collator
)

tokenizer = AutoTokenizer.from_pretrained("sarvamai/sarvam-1")
data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer)
model = AutoModelForCausalLM.from_pretrained("sarvamai/sarvam-1")
ds = datasets.load_dataset("sarvamai/samvaad-hi-v1")


# add a chat template to the tokenizer so that it can handle multi-turn conversations
tokenizer.chat_template = "{% if messages[0]['role'] == 'system' %}{% set loop_messages = messages[1:] %}{% set system_message = messages[0]['content'] %}{% else %}{% set loop_messages = messages %}{% set system_message = false %}{% endif %}{% for message in loop_messages %}{% if (message['role'] == 'user') != (loop.index0 % 2 == 0) %}{{ raise_exception('Conversation roles must alternate user/assistant/user/assistant/...') }}{% endif %}{% if loop.index0 == 0 and system_message != false %}{% set content = '<<SYS>>\\n' + system_message + '\\n<</SYS>>\\n\\n' + message['content'] %}{% else %}{% set content = message['content'] %}{% endif %}{% if message['role'] == 'user' %}{{ bos_token + '[INST] ' + content.strip() + ' [/INST]' }}{% elif message['role'] == 'assistant' %}{{ ' '  + content.strip() + ' ' + eos_token }}{% endif %}{% endfor %}"

# the tokenizer does not have a pad token, so let's add it and resize the model embeddings
tokenizer.add_tokens("[PAD]", special_tokens=True)
tokenizer.pad_token = "[PAD]"
model.resize_token_embeddings(len(tokenizer))

# let us use the parameter-efficient finetuning method LoRA
# using this config, we will only train 100M parameters (~3% of the total parameters)
config = LoraConfig(
    r=64, lora_alpha=128, lora_dropout=0.0, target_modules=["lm_head", "k_proj", "q_proj", "v_proj" "o_proj", "gate_proj", "down_proj", "up_proj"]
)
model = get_peft_model(model, config)
model.print_trainable_parameters()



# to keep things fast, let us only train on 1000 conversations
ds["train"] = ds["train"].select(range(1000))

# let us preprocess the dataset
def preprocess_function(example):
  model_inputs = tokenizer.apply_chat_template(example["messages"], tokenize=False)
  tokenized_inputs = tokenizer(model_inputs)
  tokenized_inputs["labels"] = tokenized_inputs["input_ids"].copy()
  return tokenized_inputs

ds = ds.map(preprocess_function, remove_columns=ds["train"].column_names)


# train the model
training_args = TrainingArguments(
    output_dir="sarvam-1git s-ft",
    num_train_epochs=1,
    save_total_limit=1,
    per_device_train_batch_size=1,
    warmup_steps=10,
    weight_decay=0.0001,
    bf16=True,
    logging_steps=10,
    learning_rate=1e-5,
    gradient_checkpointing=True,
    gradient_checkpointing_kwargs={"use_reentrant": False},
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=ds["train"],
    data_collator=data_collator,
)
trainer.train()


# let us now test whether the model has learned to answer questions
message = [{'role': 'user', 'content': 'भारत ने पहली बार विश्व कप कब जीता?'}]
model_input = tokenizer.apply_chat_template(message, tokenize=False)
tokenized_input = tokenizer(model_input, return_tensors='pt')
tokenized_input = tokenized_input.to("cuda")

model.eval()
output_tokens = model.generate(
    **tokenized_input,
    max_new_tokens=256,
    do_sample=True,
    temperature=0.01,
    top_p=0.95,
    top_k=50,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.pad_token_id,
)
output = tokenizer.decode(output_tokens[0], skip_special_tokens=True)
print(output)