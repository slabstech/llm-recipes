import pyttsx3
from pydub import AudioSegment

def text_to_speech(text, output_file, rate=150):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.save_to_file(text, output_file)
    engine.runAndWait()

def create_audio_drama(script_file, output_file):
    with open(script_file, 'r') as file:
        lines = file.readlines()
    
    final_audio = AudioSegment.empty()
    
    for line in lines:
        if line.strip() == '' or line.startswith('#'):
            continue
        
        parts = line.strip().split(':')
        if len(parts) == 2:
            character, dialogue = parts
            temp_file = f"{character}_temp.mp3"
            text_to_speech(dialogue, temp_file)
            
            segment = AudioSegment.from_mp3(temp_file)
            final_audio += segment + AudioSegment.silent(duration=500)
    
    final_audio.export(output_file, format="mp3")

# Usage
create_audio_drama("script.txt", "audio_drama.mp3")
