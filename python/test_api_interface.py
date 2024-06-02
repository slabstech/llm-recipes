import unittest
import json
import api_interface
from unittest.mock import Mock, patch, MagicMock
from typing import List
import pytest
import os


@pytest.fixture
def mock_spec():
    mock_spec = {
        'paths': {
            '/users/{userId}': {
                'get': {
                    'operationId': 'getUserById',
                    'description': 'Get user details by user ID',
                    'parameters': [
                        {
                            'name': 'userId',
                            'schema': {
                                'type': 'string'
                            },
                            'description': 'The ID of the user to retrieve'
                        }
                    ]
                }
            },
            '/posts/{postId}': {
                'get': {
                    'operationId': 'getPostById',
                    'description': 'Get post details by post ID',
                    'parameters': [
                        {
                            'name': 'postId',
                            'schema': {
                                'type': 'integer'
                            },
                            'description': 'The ID of the post to retrieve'
                        }
                    ]
                }
            }
        }
    }
    return mock_spec

@patch('api_interface.prance.ResolvingParser')
def test_generate_tools(mock_parser, mock_spec):
    # Arrange
    objs = [('users', 'userId'), ('posts', 'postId')]
    function_end_point = 'https://example.com/api/swagger.json'
    mock_parser_instance = Mock()
    mock_parser_instance.specification = mock_spec
    mock_parser.return_value = mock_parser_instance

    # Act
    tools = api_interface.generate_tools(objs, function_end_point)

    # Assert
    assert len(tools) == len(objs)
    assert tools[0].function.name == 'getUserById'
    assert tools[0].function.description == 'Get user details by user ID'
    assert tools[0].function.parameters == {
        'type': 'object',
        'properties': {
            'userId': {
                'type': 'string',
                'description': 'The ID of the user to retrieve'
            }
        },
        'required': ['userId']
    }
    assert tools[1].function.name == 'getPostById'
    assert tools[1].function.description == 'Get post details by post ID'
    assert tools[1].function.parameters == {
        'type': 'object',
        'properties': {
            'postId': {
                'type': 'integer',
                'description': 'The ID of the post to retrieve'
            }
        },
        'required': ['postId']
    }


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


@pytest.fixture
def sample_queries() -> List[str]:
    return ["Hello", "How are you?", "What's the weather like today?"]

def test_get_user_messages(sample_queries):
    # Act
    user_messages = api_interface.get_user_messages(sample_queries)

    # Assert
    assert len(user_messages) == len(sample_queries)
    for i, query in enumerate(sample_queries):
        assert user_messages[i].content == query

def test_get_user_messages_empty_list():
    # Act
    user_messages = api_interface.get_user_messages([])

    # Assert
    assert len(user_messages) == 0

def test_get_user_messages_single_query():
    # Arrange
    query = "Hello, world!"

    # Act
    user_messages = api_interface.get_user_messages([query])

    # Assert
    assert len(user_messages) == 1
    assert user_messages[0].content == query


@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv('OLLAMA_ENDPOINT', 'http://mock-endpoint:1234')

@patch('api_interface.requests.post')
def test_execute_generator(mock_post, mock_env_vars):
    # Arrange
    mock_response = Mock()
    mock_response.json.return_value = {'result': 'mock_result'}
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # Act
    api_interface.execute_generator()

    # Assert
    mock_post.assert_called_once_with(
        'http://mock-endpoint:1234/api/generate',
        json={
            'model': 'mistral:7b',
            'prompt': mock.ANY,
            'stream': False,
            'raw': True
        },
        stream=False
    )
    process_results.assert_called_once_with(mock_response.json(), mock.ANY)

@patch('api_interface.get_user_messages')
@patch('api_interface.generate_tools')
def test_execute_generator_helper_functions(mock_generate_tools, mock_get_user_messages, mock_env_vars):
    # Arrange
    mock_user_messages = ['mock_user_message']
    mock_user_tools = ['mock_user_tool']
    mock_get_user_messages.return_value = mock_user_messages
    mock_generate_tools.return_value = mock_user_tools

    # Act
    api_interface.execute_generator()

    # Assert
    mock_get_user_messages.assert_called_once_with(["What's the status of my Pet 1?", "Find information of user user1?", "What's the status of my Store Order 3?"])
    mock_generate_tools.assert_called_once_with([['pet', 'petId'], ['user', 'username'], ['store/order', 'orderId']], 'https://petstore3.swagger.io/api/v3/openapi.json')


if __name__ == '__main__':
    unittest.main()
