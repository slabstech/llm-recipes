from  ....notebooklm.tts_generator import tts_server_batch
#Batch Speech Generatioon

texts = ["Hey, how are you doing?", "I'm not sure how to feel about it."]
speaker_descriptions = "A male speaker with a monotone and high-pitched voice is delivering his speech at a really low speed in a confined environment."


length_of_input_text = len(texts)


# Create the description list with the same length as input_text
description = [speaker_descriptions] * length_of_input_text
audio_segments = tts_server_batch(texts, description)
for i, audio in enumerate(audio_segments):
    print(f"Audio {i}: {audio}")
