import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"


def voice_clone(query_text, speaker_voice_sample):
    output_file_name="clone_voice_output.wav"
    tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
    tts.tts_with_vc_to_file(
        query_text,
        speaker_wav=speaker_voice_sample,
        file_path="cloned_voice_output.wav"
    )
    return output_file_name

def text_to_speech(query_text):
    output_file_name="voice_output.wav"
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False).to(device)

    # Run TTS
    tts.tts_to_file(text=query_text, file_path=output_file_name)
    return output_file_name

def main():
    ai_barcamp_text = "This is an example of text to speech for AI barcamp project demo."
    text_to_speech(ai_barcamp_text)

    query_text ="My name is Sachin Shetty?, What is your name?"

    speaker_voice_sample = "voice_input.wav"
    voice_clone(query_text, speaker_voice_sample)


if __name__ == "__main__":
    main()