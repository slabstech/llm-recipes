import unittest
from unittest.mock import patch, Mock
from speech_to_speech_inference import main

class TestSpeechToSpeechInference(unittest.TestCase):
    @patch('speech_to_speech_inference.voice_capture')
    @patch('speech_to_speech_inference.voice_query')
    @patch('speech_to_speech_inference.execute_generator')
    @patch('speech_to_speech_inference.text_to_speech')
    def test_main(self, mock_text_to_speech, mock_execute_generator, mock_voice_query, mock_voice_capture):
        # Set up the mock responses
        mock_voice_query.return_value = "What is the status of order 123?"
        mock_execute_generator.return_value = "The order is currently being processed."
        mock_text_to_speech.return_value = "voice_output.wav"

        # Call the main function
        main()

        # Check that the functions were called correctly
        mock_voice_capture.assert_called_once_with("voice_input.wav")
        mock_voice_query.assert_called_once_with("voice_input.wav")
        mock_execute_generator.assert_called_once_with(["What is the status of order 123?"], [['pet','petId'], ['user', 'username'], ['store/order','orderId']])
        mock_text_to_speech.assert_called_once_with(query_text="The order is currently being processed.")

if __name__ == '__main__':
    unittest.main()
