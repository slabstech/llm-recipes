import unittest
from unittest.mock import patch, MagicMock
import os
from your_module import text_to_speech, voice_clone  # replace 'your_module' with the name of the module containing your functions

class TestVoiceOutput(unittest.TestCase):
    @patch('your_module.TTS')
    def test_text_to_speech(self, mock_tts):
        # Set up the mock TTS object
        mock_tts_instance = MagicMock()
        mock_tts.return_value = mock_tts_instance

        # Call the function
        result = text_to_speech('test text')

        # Check the result
        self.assertEqual(result, 'voice_output.wav')
        mock_tts_instance.tts_to_file.assert_called_once_with(text='test text', file_path='voice_output.wav')

        # Clean up
        if os.path.exists('voice_output.wav'):
            os.remove('voice_output.wav')

    @patch('your_module.TTS')
    def test_voice_clone(self, mock_tts):
        # Set up the mock TTS object
        mock_tts_instance = MagicMock()
        mock_tts.return_value = mock_tts_instance

        # Call the function
        result = voice_clone('test text', 'test_voice_sample.wav')

        # Check the result
        self.assertEqual(result, 'clone_voice_output.wav')
        mock_tts_instance.tts_with_vc_to_file.assert_called_once_with(
            'test text',
            speaker_wav='test_voice_sample.wav',
            file_path='cloned_voice_output.wav'
        )

        # Clean up
        if os.path.exists('cloned_voice_output.wav'):
            os.remove('cloned_voice_output.wav')

if __name__ == '__main__':
    unittest.main()
