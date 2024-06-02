import whisper
model = whisper.load_model("small")
result = model.transcribe("audio.mp3")
print(result["text"])
print(result)