from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer, AutoFeatureExtractor, set_seed
import scipy
import soundfile as sf

repo_id = "parler-tts/parler-tts-mini-v1"

model = ParlerTTSForConditionalGeneration.from_pretrained(repo_id).to("cuda")
tokenizer = AutoTokenizer.from_pretrained(repo_id, padding_side="left")
feature_extractor = AutoFeatureExtractor.from_pretrained(repo_id)

input_text = ["Hey, how are you doing?", "I'm not sure how to feel about it.",  "When we look back on these days, When the stories are" ,
              "All that remain, Will we be more, Than the voices in our heads? ", "What will we spend on regret? ,How far will we go to forget?",
              " Baby it's too soon to tell, Where the story will end"]

description_text = "Jon's voice is monotone yet slightly fast in delivery, with a very close recording that almost has no background noise."

# Determine the length of the input_text list
length_of_input_text = len(input_text)

# Create the description list with the same length as input_text
description = [description_text] * length_of_input_text

inputs = tokenizer(description, return_tensors="pt", padding=True).to("cuda")
prompt = tokenizer(input_text, return_tensors="pt", padding=True).to("cuda")

set_seed(0)
generation = model.generate(
    input_ids=inputs.input_ids,
    attention_mask=inputs.attention_mask,
    prompt_input_ids=prompt.input_ids,
    prompt_attention_mask=prompt.attention_mask,
    do_sample=True,
    return_dict_in_generate=True,
)

response_format = 'wav'

for i, audio in enumerate(generation.sequences):
    audio_arr = audio[:generation.audios_length[i]].cpu().numpy().squeeze()
    file_path = f"out_{i}.{response_format}"
    sf.write(file_path, audio_arr, model.config.sampling_rate)
'''    
audio_1 = generation.sequences[0, :generation.audios_length[0]]
audio_2 = generation.sequences[1, :generation.audios_length[1]]

print(audio_1.shape, audio_2.shape)
scipy.io.wavfile.write("sample_out.wav", rate=feature_extractor.sampling_rate, data=audio_1.cpu().numpy().squeeze())
scipy.io.wavfile.write("sample_out_2.wav", rate=feature_extractor.sampling_rate, data=audio_2.cpu().numpy().squeeze())
'''