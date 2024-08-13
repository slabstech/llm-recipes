import transformers
import librosa

# load the model pipeline on gpu:0
pipe = transformers.pipeline(model='sarvamai/shuka_v1', trust_remote_code=True, device=0)

# get a sample audio
# wget https://huggingface.co/sarvamai/shuka_v1/resolve/main/hi-question.webm

audio, _ = librosa.load("./hi-question.webm", sr=16000)
turns = [
          {'role': 'system', 'content': 'Respond naturally and informatively.'},
          {'role': 'user', 'content': '<|audio|>'}
        ]

pipe({'audio': audio, 'turns': turns, 'sampling_rate': sr}, max_new_tokens=512)
