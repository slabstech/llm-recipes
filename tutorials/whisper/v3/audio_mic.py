import io
import time
import httpx
import sounddevice as sd
import wavio

# Parameters
duration = 5  # seconds per chunk
sample_rate = 16000
channels = 1

print("Starting continuous recording and transcription. Press Ctrl+C to stop.")

try:
    while True:
        print("\nRecording...")
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
        sd.wait()

        print("Sending audio for transcription...")

        wav_io = io.BytesIO()
        wavio.write(wav_io, audio_data, sample_rate, sampwidth=2)
        wav_io.seek(0)

        files = {
            'file': ('microphone.wav', wav_io, 'audio/wav'),
            'model': (None, 'Systran/faster-whisper-small')
        }

        response = httpx.post('https://dwani-whisper.hf.space/v1/audio/transcriptions', files=files)

        if response.status_code == 200:
            print("Transcription:", response.text)
        else:
            print(f"Error: {response.status_code} - {response.text}")

        # Optional: small pause before next recording, or start immediately
        # time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopped by user.")
