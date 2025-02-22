import pytest
from api import fetch_menu_from_api, authenticate, fetch_user_credentials_from_api, submit_order
from unittest.mock import patch, Mock

restaurants_sample = {
    "rest1": {
        "name": "The Rameshwaram Cafe",
        "opening_hours": "6am – 12midnight",
        "menu": {"Idli & Vada": [{"id": "1", "name": "Butter Idli", "price": 100.0}]}
    }
}

@patch("api.requests.get")
def test_fetch_menu_from_api(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "restaurants": restaurants_sample}
    mock_get.return_value = mock_response
    error, restaurants = fetch_menu_from_api("token123")
    assert error is None
    assert "rest1" in restaurants
    assert restaurants["rest1"]["name"] == "The Rameshwaram Cafe"

@patch("api.requests.get")
def test_fetch_menu_from_api_error(mock_get):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = "Server error"
    mock_response.raise_for_status.side_effect = requests.RequestException("Server error")
    mock_get.return_value = mock_response
    error, restaurants = fetch_menu_from_api("token123")
    assert error == "Sorry, I couldn't connect to the menu service. Please try again later."
    assert restaurants == {}

@patch("api.requests.post")
def test_authenticate(mock_post):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "token123"}
    mock_post.return_value = mock_response
    token = authenticate("user1", "password123")
    assert token == "token123"

@patch("api.requests.post")
def test_authenticate_failure(mock_post):
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = requests.RequestException("Unauthorized")
    mock_post.return_value = mock_response
    token = authenticate("user1", "wrongpass")
    assert token is None