from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM, AutoModel
import torch

# Load the T5 encoder (text encoder)
text_encoder_name = "google/flan-t5-large"  # From the config
text_tokenizer = AutoTokenizer.from_pretrained(text_encoder_name)
text_encoder = AutoModelForSeq2SeqLM.from_pretrained(text_encoder_name)

# Load the Decoder (ParlerTTSForCausalLM - custom)
decoder_name = "parler-tts/parler-tts-mini-v1.1" #Or the local path to the decoder
decoder = AutoModelForCausalLM.from_pretrained(decoder_name)

# Load the Audio Encoder (DAC)
audio_encoder_name = "ylacombe/dac_44khz"
audio_encoder = AutoModel.from_pretrained(audio_encoder_name) # Using AutoModel as it might not be seq2seq or causal LM

# Set to eval mode
text_encoder.eval()
decoder.eval()
audio_encoder.eval()
