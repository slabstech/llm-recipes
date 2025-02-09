import argparse
from script_parser import script_parser
from tts_generator import speech_generator
import time

def main(language):

    language = 'en'

    start_time = time.time()
    if language == 'en':
        file_name = 'audiobook/resources/Skript-Go-Audio-Eng.pdf'
    elif language == 'de':
        file_name = 'audiobook/resources/Skript-Go-Audio-De.pdf'
    else:
        raise ValueError("Unsupported language. Please choose 'en' for English or 'de' for German.")
    
    file_name = 'audiobook/resources/Skript-Go-Audio-De.pdf'

    # TODO - remove hardcoded voices for specific speaker
    ## Use Jon for Narrator voice,  Mike for leo and, Laura for Emma. Hardocoded for now

    script_parser_start = time.time()

    script_parser(language= language, file_name= file_name)

    script_parser_end = time.time()

    speech_generator_start = time.time()


    speech_generator(language)
    speech_generator_end = time.time()


    end_time = time.time()

    total_time = end_time - start_time
    script_parser_time = script_parser_end - script_parser_start
    speech_generator_time = speech_generator_end - speech_generator_start

    print(f"Total execution time: {total_time:.2f} seconds")
    print(f"Script parsing time: {script_parser_time:.2f} seconds")
    print(f"Speech generation time: {speech_generator_time:.2f} seconds")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audiobook Creation from Script")
    parser.add_argument('--language', type=str, default='en', help='Language code for the prompts (e.g., en, fr, de, es, it, nl, pt, sv)')
    args = parser.parse_args()
    main(args.language)