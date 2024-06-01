import unittest
import json
from unittest.mock import patch, MagicMock
from api_interface import process_results

class TestProcessResults(unittest.TestCase):
    def setUp(self):
        self.result = {
            "response": "[TOOL_CALLS] [{'name': 'search_quality_reflection', 'arguments': {'query': 'How to write good unit tests in Python'}}, {'name': 'search_quality_score', 'arguments': {'query': 'How to write good unit tests in Python'}}]\n\nSearch quality reflection: Writing good unit tests in Python involves following best practices such as...\n\nSearch quality score: 4"
        }
        self.messages = [MagicMock(), MagicMock()]
        self.names_to_functions = {
            "search_quality_reflection": lambda **kwargs: "Reflection result",
            "search_quality_score": lambda **kwargs: 4
        }

    @patch('builtins.print')
    def test_process_results(self, mock_print):
        process_results(self.result, self.messages)

        # Assert tool calls are split correctly
        mock_print.assert_any_call(self.messages[0].content)
        mock_print.assert_any_call("Reflection result")
        mock_print.assert_any_call(self.messages[1].content)
        mock_print.assert_any_call(4)

    def test_process_results_with_undefined_function(self):
        self.result["response"] = "[TOOL_CALLS] [{'name': 'undefined_function', 'arguments': {}}]\n\n"

        with self.assertLogs() as captured:
            process_results(self.result, self.messages)

        self.assertEqual(captured.records[0].getMessage(), "undefined_function is not defined")

    def test_process_results_with_invalid_json(self):
        self.result["response"] = "Invalid JSON"

        with self.assertRaises(json.JSONDecodeError):
            process_results(self.result, self.messages)


import unittest
from unittest.mock import patch

def process_results(result, messages):
    # ... (function code)


    @patch('__main__.names_to_functions', {
        'search_quality_reflection': lambda **kwargs: 'Reflection result',
        'search_quality_score': lambda **kwargs: 4
    })
    def test_process_results(self, mock_names_to_functions):
        result = {
            "response": "[TOOL_CALLS] [{'name': 'search_quality_reflection', 'arguments': {'query': 'How to write good unit tests in Python'}}, {'name': 'search_quality_score', 'arguments': {'query': 'How to write good unit tests in Python'}}]\n\nSearch quality reflection: Writing good unit tests in Python involves following best practices such as...\n\nSearch quality score: 4"
        }
        messages = [unittest.mock.MagicMock(), unittest.mock.MagicMock()]

        with unittest.mock.patch('builtins.print') as mock_print:
            process_results(result, messages)

        mock_print.assert_any_call(messages[0].content)
        mock_print.assert_any_call('Reflection result')
        mock_print.assert_any_call(messages[1].content)
        mock_print.assert_any_call(4)


if __name__ == '__main__':
    unittest.main()
