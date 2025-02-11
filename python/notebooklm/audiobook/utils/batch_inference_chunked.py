from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer, AutoFeatureExtractor, set_seed
import soundfile as sf
import time
import numpy as np

# Define a function to split text into smaller chunks
def chunk_text(text, chunk_size):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(' '.join(words[i:i + chunk_size]))
    return chunks

try:

    repo_id = "parler-tts/parler-tts-mini-v1.1"

    start_time = time.time()

    model = ParlerTTSForConditionalGeneration.from_pretrained(repo_id).to("cuda")
    tokenizer = AutoTokenizer.from_pretrained(repo_id, padding_side="left")
    feature_extractor = AutoFeatureExtractor.from_pretrained(repo_id)

    input_text = ["Hey, how are you doing?", "I'm not sure how to feel about it.", "When we look back on these days, When the stories are",
                "All that remain, Will we be more, Than the voices in our heads? ", "What will we spend on regret? ,How far will we go to forget?",
                " Baby it's too soon to tell, Where the story will end,Baby it's too soon to tell, Where the story will end,Baby it's too soon to tell, Where the story will end,Baby it's too soon to tell, Where the story will end,Baby it's too soon to tell, Where the story will end,Baby it's too soon to tell, Where the story will end,Baby it's too soon to tell, Where the story will end,Baby it's too soon to tell, Where the story will end,Baby it's too soon to tell, Where the story will end, "]

    description_text = "Jon's voice is monotone yet slightly fast in delivery, with a very close recording that almost has no background noise."

    # Determine the length of the input_text list
    length_of_input_text = len(input_text)
 
    # Create the description list with the same length as input_text
    description = [description_text] * length_of_input_text

    description_tokenizer = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)
    length_of_input_text = len(input_text)

    # Set chunk size for text processing
    chunk_size = 15  # Adjust this value based on your needs

    # Prepare inputs for the model
    all_chunks = []
    all_descriptions = []
    for i, text in enumerate(input_text):
        chunks = chunk_text(text, chunk_size)
        all_chunks.extend(chunks)
        all_descriptions.extend([description[i]] * len(chunks))

    description_inputs = description_tokenizer(all_descriptions, return_tensors="pt", padding=True).to("cuda")
    prompts = tokenizer(all_chunks, return_tensors="pt", padding=True).to("cuda")

    set_seed(0)
    generation = model.generate(
        input_ids=description_inputs.input_ids,
        attention_mask=description_inputs.attention_mask,
        prompt_input_ids=prompts.input_ids,
        prompt_attention_mask=prompts.attention_mask,
        do_sample=True,
        return_dict_in_generate=True,
    )

    # Concatenate audio outputs
    audio_outputs = []
    current_index = 0
    for i, text in enumerate(input_text):
        chunks = chunk_text(text, chunk_size)
        chunk_audios = []
        for j in range(len(chunks)):
            audio_arr = generation.sequences[current_index][:generation.audios_length[current_index]].cpu().numpy().squeeze()
            chunk_audios.append(audio_arr)
            current_index += 1
        combined_audio = np.concatenate(chunk_audios)
        audio_outputs.append(combined_audio)

    # Save the final audio outputs
    response_format = 'wav'
    for i, audio in enumerate(audio_outputs):
        file_path = f"generated/out_{i}.{response_format}"
        sf.write(file_path, audio, model.config.sampling_rate)
        print(f"Processed chunk {i+1}/{length_of_input_text} and saved to {file_path}")

    end_time = time.time()

    total_time = end_time - start_time

    print(f"Total execution time: {total_time:.2f} seconds")

except KeyError as e:
    print(f"KeyError: {e} - The key does not exist in the JSON data.")
except TypeError as e:
    print(f"TypeError: {e} - Ensure the JSON data is correctly loaded into a dictionary.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")