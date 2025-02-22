import pytest
from llm import parse_and_search_order
from unittest.mock import patch, MagicMock

# Sample data
restaurants_sample = {
    "rest1": {
        "name": "The Rameshwaram Cafe",
        "menu": {"Idli & Vada": [{"id": "1", "name": "Butter Idli", "price": 100.0}]},
    }
}


@patch("llm.client.chat")
def test_parse_and_search_order_valid(mock_chat):
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content='[{"item": "Butter Idli", "quantity": 1}]'))
    ]
    mock_chat.complete.return_value = mock_response
    feedback, order = parse_and_search_order("1 Butter Idli", restaurants_sample)
    assert (
        "Added 1 x Butter Idli (from The Rameshwaram Cafe) to your order." in feedback
    )
    assert order == {"rest1:Idli & Vada:1": 1}


@patch("llm.client.chat")
def test_parse_and_search_order_invalid(mock_chat):
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content='{"error": "Item not found"}'))
    ]
    mock_chat.complete.return_value = mock_response
    feedback, order = parse_and_search_order("1 Ghee Idli", restaurants_sample)
    assert (
        feedback
        == "Sorry, I couldn't understand your order: Item not found. Please try rephrasing it (e.g., '2 Butter Idlis')."
    )
    assert order == {}


@patch("llm.client.chat")
def test_parse_and_search_order_empty_response(mock_chat):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=""))]
    mock_chat.complete.return_value = mock_response
    feedback, order = parse_and_search_order("1 Butter Idli", restaurants_sample)
    assert (
        feedback
        == "Oops, something went wrong while understanding your order. Please try again or simplify your request (e.g., '1 Butter Idli')."
    )
    assert order == {}
