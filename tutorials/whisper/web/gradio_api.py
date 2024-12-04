from gradio_client import Client

client = Client("https://openai-whisper.hf.space/")
result = client.predict(
				"https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav",	# str (filepath or URL to file) in 'inputs' Audio component
				"transcribe",	# str in 'Task' Radio component
				api_name="/predict"
)
print(result)