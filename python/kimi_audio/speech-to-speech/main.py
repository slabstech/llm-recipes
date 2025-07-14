def client_send_handshake(audio_connection):
    print("client -sending handhsake")
    audio_connection = {"client_connection":"true"}
    return audio_connection

def server_receive_handshake(audio_connection):
    print("server-receive_handhsake")
    audio_connection_new = {"server_connection":"true"}

    audio_connection |= audio_connection_new
    return audio_connection



import torch
import torchaudio

def create_audio_chunks(file_path, chunk_duration_sec=1):
    # Load audio file (waveform shape: [channels, samples])
    waveform, sample_rate = torchaudio.load(file_path)
    
    # Calculate chunk size in samples
    chunk_size = int(sample_rate * chunk_duration_sec)
    total_samples = waveform.size(1)
    
    chunks = []
    start = 0
    
    # Slice waveform into chunks
    while start < total_samples:
        end = min(start + chunk_size, total_samples)
        chunk = waveform[:, start:end]
        chunks.append(chunk)
        start = end
    
    return chunks, sample_rate


def save_chunks(chunks, sample_rate, prefix="chunk"):

    for i, chunk in enumerate(chunks):
        # Save each chunk as a separate WAV file
        filename = f"{prefix}_{i+1}.wav"
        torchaudio.save(filename, chunk, sample_rate)
        print(f"Saved {filename} with shape {chunk.shape}")

def client_send_audio_chunk(audio_connection, audio_files):
    print("cleint send audio chunk")
    audio_connection_new = {"client_send_audio_chunk=1":"true"}

    audio_path = audio_files['file'][0] # "kannada_sample.wav"  # Replace with your audio file path
    chunk_duration = 1  # seconds
    
    chunks, sr = create_audio_chunks(audio_path, chunk_duration)
    print(f"Total chunks created: {len(chunks)}")
    
    save_chunks(chunks, sr, audio_path)


    audio_connection |= audio_connection_new
    return audio_connection


import torchaudio

def stream_audio_chunks(source, chunk_size=16000):
    """
    Stream audio chunks from a source using torchaudio StreamReader.

    Args:
        source (str): Path, URL, or device identifier for the audio source.
        chunk_size (int): Number of frames per chunk (samples per channel).

    Yields:
        Tensor: Audio chunk tensor of shape (chunk_size, channels).
    """
    # Create StreamReader for the source
    reader = torchaudio.io.StreamReader(source)

    # Add an audio stream with desired chunk size (frames_per_chunk)
    # You can specify sample_rate here if you want resampling
    reader.add_audio_stream(frames_per_chunk=chunk_size)

    # Start streaming chunks
    while True:
        # Fill buffer with decoded frames
        try:
            reader.fill_buffer()
        except RuntimeError as e:
            if "End of file" in str(e):
                break
            else:
                raise()

        # Pop chunks (list of tensors, one per output stream)
        chunks = reader.pop_chunks()
        if not chunks:
            # No more chunks, end of stream
            break

        audio_chunk = chunks[0]  # since we added only one audio stream

        # audio_chunk shape: (frames_per_chunk, channels)
        yield audio_chunk

import openai
import io


def tensor_to_wav_bytes(tensor, sample_rate=16000):
    """
    Convert a (frames, channels) int16 tensor to WAV bytes.
    """
    # Ensure tensor is CPU and int16
    if tensor.dtype != torch.int16:
        tensor = tensor.to(torch.int16)
    tensor = tensor.cpu()

    # Use torchaudio to encode to WAV in-memory
    buffer = io.BytesIO()
    # torchaudio expects (channels, frames)
    tensor = tensor.T
    torchaudio.save(buffer, tensor, sample_rate=sample_rate, format="wav")
    buffer.seek(0)
    return buffer.read()



import requests
def chunk_stream():
    audio_source = "english_sample.wav"  # Replace with your audio source

    # Example: chunk size of 1 second assuming 16 kHz sample rate
    chunk_size = 16000

    for i, chunk in enumerate(stream_audio_chunks(audio_source, chunk_size)):
        print(f"Chunk {i+1}: shape={chunk.shape}, dtype={chunk.dtype}")
        # Here you can process the chunk (e.g., feature extraction, model input, etc.)

        wav_bytes = tensor_to_wav_bytes(chunk, sample_rate=16000)

        url = "http://127.0.0.1:8000/v1/audio/transcriptions"

        files = {
            "file": ("chunk.wav", wav_bytes, "audio/wav")        }

        data = {
            "model": "whisper-1"
        }

        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        transcription = response.json()
        #print(response.json())


        # Send to OpenAI Whisper API
        print(f"Transcription for chunk {i+1}: {transcription}")



def server_receive_audio_chunk(audio_connection):
    print("server receive audio chunk")
    audio_connection_new = {"server_receive_audio_chunk=1":"true"}

    audio_connection |= audio_connection_new
    return audio_connection


def server_send_vad_commit_message(audio_connection):
    print("server_send_vad_commit_message")
    audio_connection_new = {"server_send_vad_commit_message":"true"}

    audio_connection |= audio_connection_new
    return audio_connection


def client_receive_vad_message(audio_connection):
    print("client_receive_vad_message")

    audio_connection_new = {"client_receive_vad_message":"true"}

    audio_connection |= audio_connection_new
    return audio_connection

def server_send_audio_chunk(audio_connection):
    print("server_send_audio_chunk")
    audio_connection_new = {"server_send_audio_chunk=1":"true"}

    audio_connection |= audio_connection_new
    return audio_connection

def client_receive_audio_chunk(audio_connection):
    print("client_receive_audio_chunk")

    audio_connection_new = {"client_receive_audio_chunk=1":"true"}

    audio_connection |= audio_connection_new
    return audio_connection

def server_send_finish(audio_connection):
    print("server_send_finish")
    audio_connection_new = {"server_send_finish":"true"}

    audio_connection |= audio_connection_new
    return audio_connection

def client_receive_finish(audio_connection):
    print("client_receive_finish")
    audio_connection_new = {"client_receive_finish":"true"}

    audio_connection |= audio_connection_new
    return audio_connection


def client_end_connection(audio_connection):
    print("client_end_connection")
    audio_connection_new = {"client_end_connection":"true"}

    audio_connection |= audio_connection_new
    return audio_connection

def server_end_connection(audio_connection):
    print("server_end_connection")
    audio_connection_new = {"server_end_connection":"true"}

    audio_connection |= audio_connection_new
    return audio_connection



def main():
    print("hwllo_wolrd")

    audio_connection={}

    audio_connection=client_send_handshake(audio_connection)

    print(audio_connection)
    server_receive_handshake(audio_connection)

    print(audio_connection)

    audio_file_name = 'kannada_sample.wav'
    with open(audio_file_name, 'rb') as f:
        audio_file = {
            'file': (audio_file_name, f),
    }
        
    #client_send_audio_chunk(audio_connection, audio_file)

    chunk_stream()

''' audio_file_name = 'english_sample.wav'
    with open(audio_file_name, 'rb') as f:
        audio_file = {
            'file': (audio_file_name, f),
    }
        
    client_send_audio_chunk(audio_connection, audio_file)
'''
   


'''

    print(audio_connection)

    server_receive_audio_chunk(audio_connection)

    print(audio_connection)

    #client_send_audio_chunk(audio_connection)

    #print(audio_connection)

    server_receive_audio_chunk(audio_connection)

    print(audio_connection)

    server_send_vad_commit_message(audio_connection)
    print(audio_connection)



    client_receive_vad_message(audio_connection)

    print(audio_connection)

    server_send_audio_chunk(audio_connection)

    print(audio_connection)

    client_receive_audio_chunk(audio_connection)

    print(audio_connection)

    server_send_audio_chunk(audio_connection)

    print(audio_connection)
    client_receive_audio_chunk(audio_connection)
    print(audio_connection)
    server_send_audio_chunk(audio_connection)
    print(audio_connection)
    client_receive_audio_chunk(audio_connection)
    print(audio_connection)

    server_send_finish(audio_connection)
    print(audio_connection)
    client_receive_finish(audio_connection)
    print(audio_connection)

    client_end_connection(audio_connection)
    print(audio_connection)

    server_end_connection(audio_connection)
'''    
if __name__ == "__main__":
    main()
