import unittest
from unittest.mock import patch, Mock
from vision_query import explain_image

class TestExplainImage(unittest.TestCase):
    @patch('requests.post')
    def test_explain_image(self, mock_post):
        # Set up the mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.iter_lines.return_value = [b'{"response": "The image contains a computer screen with text."}']
        mock_post.return_value = mock_response

        # Call the function
        explain_image("test_image.png", "moondream", "What is in this image?", "http://localhost:11434")

        # Check that the function made the correct request
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "http://localhost:11434/api/chat")
        self.assertIn("messages", kwargs["json"])
        self.assertEqual(kwargs["json"]["messages"][0]["content"], "What is in this image?")

if __name__ == '__main__':
    unittest.main()
