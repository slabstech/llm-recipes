import argparse
from script_parser import script_parser
from tts_generator import speech_generator

def main(language):

    file_name = 'audiobook/resources/Skript-GoAudio-Eng.pdf'

    # TODO - remove hardcoded voices for specific speaker
    ## Use Jon for Narrator voice,  Mike for leo and, Laura for Emma. Hardocoded for now

    #script_parser(language= language, file_name= file_name)
    speech_generator()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audiobook Creation from Script")
    parser.add_argument('--language', type=str, default='en', help='Language code for the prompts (e.g., en, fr, de, es, it, nl, pt, sv)')
    args = parser.parse_args()
    main(args.language)