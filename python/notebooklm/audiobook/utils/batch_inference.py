from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer, AutoFeatureExtractor, set_seed
import scipy


repo_id = "parler-tts/parler-tts-mini-v1"

model = ParlerTTSForConditionalGeneration.from_pretrained(repo_id).to("cuda")
tokenizer = AutoTokenizer.from_pretrained(repo_id, padding_side="left")
feature_extractor = AutoFeatureExtractor.from_pretrained(repo_id)

input_text = ["Hey, how are you doing?", "I'm not sure how to feel about it."]
description = 2 * ["A male speaker with a monotone and high-pitched voice is delivering his speech at a really low speed in a confined environment."]

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

audio_1 = generation.sequences[0, :generation.audios_length[0]]
audio_2 = generation.sequences[1, :generation.audios_length[1]]

print(audio_1.shape, audio_2.shape)
scipy.io.wavfile.write("sample_out.wav", rate=feature_extractor.sampling_rate, data=audio_1.cpu().numpy().squeeze())
scipy.io.wavfile.write("sample_out_2.wav", rate=feature_extractor.sampling_rate, data=audio_2.cpu().numpy().squeeze())