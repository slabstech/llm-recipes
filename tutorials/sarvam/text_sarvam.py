#from transformers import pipeline
#pipe = pipeline(model='sarvamai/sarvam-2b-v0.5', device=0)
#pipe('भारत के प्रथम प्रधानमंत्री', max_new_tokens=15, temperature=0.1, repetition_penalty=1.2)[0]['generated_text']
# 'भारत के प्रथम प्रधानमंत्री जवाहरलाल नेहरू की बेटी इंदिरा गांधी थीं।\n\n'


from transformers import pipeline

# Initialize the pipeline
pipe = pipeline(task="text-generation", model="sarvamai/sarvam-2b-v0.5", device=0)

# Generate text
prompt = "भारत के प्रथम प्रधानमंत्री"
output = pipe(prompt, max_new_tokens=15, temperature=0.1, repetition_penalty=1.2)

# Print the generated text
print(output[0]['generated_text'])



prompt_kannada= "ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ ಯಾವುದು?"
output = pipe(prompt_kannada, max_new_tokens=15, temperature=0.1, repetition_penalty=1.2)

# Print the generated text
print(output[0]['generated_text'])



prompts = ["प्रथम प्रधानमंत्री", "भारत की राजधानी", "हिंदी भाषा"]
outputs = pipe(prompts, max_new_tokens=15, temperature=0.1, repetition_penalty=1.2, batch_size=2)

for output in outputs:
    print(output['generated_text'])


from datasets import Dataset

# Create a dataset
data = Dataset.from_dict({"text": ["प्रथम प्रधानमंत्री", "भारत की राजधानी", "हिंदी भाषा"]})

# Use the dataset with the pipeline
outputs = pipe(data["text"], max_new_tokens=15, temperature=0.1, repetition_penalty=1.2, batch_size=2)

for output in outputs:
    print(output['generated_text'])
