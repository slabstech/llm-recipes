from voice_input import voice_capture
from voice_output import text_to_speech, voice_clone
from voice_query import voice_query
from api_interface import execute_generator

def main():
    voice_input_file_name = "voice_input.wav"
    voice_capture(voice_input_file_name)
    voice_response = voice_query(voice_input_file_name)
    print("speech recognition output- " + voice_response)
    queries = []
    queries.append(voice_response)
    return_objs = [['pet','petId'], ['user', 'username'], ['store/order','orderId']]

    query_result = execute_generator(queries, return_objs)
    voice_output_file_name=text_to_speech(query_text=query_result)
    print(voice_output_file_name)

if __name__ == "__main__":
    main()
