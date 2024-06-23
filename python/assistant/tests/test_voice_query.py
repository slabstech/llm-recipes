import unittest
from unittest.mock import patch, Mock
from voice_query import voice_query

class TestVoiceQuery(unittest.TestCase):
    @patch('voice_query.requests.post')
    def test_voice_query(self, mock_post):
        # Mock the response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"results": [{"transcript": "test transcript"}]}'

        # Configure the mock to return our response
        mock_post.return_value = mock_response

        # Call the function
        result = voice_query('output.wav')

        # Check that the function returned the correct result
        self.assertEqual(result, "test transcript")

if __name__ == '__main__':
    unittest.main()
