from transformers import pipeline
pipe = pipeline(model='sarvamai/sarvam-2b-v0.5', device=0)
pipe('भारत के प्रथम प्रधानमंत्री', max_new_tokens=15, temperature=0.1, repetition_penalty=1.2)[0]['generated_text']
# 'भारत के प्रथम प्रधानमंत्री जवाहरलाल नेहरू की बेटी इंदिरा गांधी थीं।\n\n'
