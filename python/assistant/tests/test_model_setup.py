import unittest
from unittest.mock import patch
import requests
from your_module import load_model  # replace 'your_module' with the name of the module containing your function

class TestLoadModel(unittest.TestCase):
    @patch('requests.post')
    def test_load_model(self, mock_post):
        # Set up the mock response
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"status": "success", "message": "Model loaded successfully"}'
        mock_post.return_value = mock_response

        # Call the function
        load_model('http://localhost:11434', 'mistral')

        # Check that the function made the correct POST request
        mock_post.assert_called_once_with(
            'http://localhost:11434/api/pull',
            json={'name': 'mistral:latest'},
            headers={'Content-Type': 'application/json'}
        )

if __name__ == '__main__':
    unittest.main()
