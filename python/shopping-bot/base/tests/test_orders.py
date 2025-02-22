import pytest
from orders import generate_order_summary, remove_item_from_order, process_order, display_menu
from db import load_state, save_state
from unittest.mock import patch

# Sample data for testing
restaurants_sample = {
    "rest1": {
        "name": "The Rameshwaram Cafe",
        "opening_hours": "6am – 12midnight",
        "menu": {
            "Idli & Vada": [
                {"id": "1", "name": "Butter Idli", "price": 100.0}
            ]
        }
    }
}
order_sample = {"rest1:Idli & Vada:1": 2}

def test_generate_order_summary():
    result = generate_order_summary(order_sample, restaurants_sample)
    expected = "=== Current Order ===\nButter Idli x2 (from The Rameshwaram Cafe) - $200.00\nTotal: $200.00"
    assert result == expected

def test_generate_order_summary_empty():
    result = generate_order_summary({}, restaurants_sample)
    assert result == "No items in your order."

def test_remove_item_from_order():
    order = order_sample.copy()
    result = remove_item_from_order("Butter Idli", order, restaurants_sample)
    assert result == "Removed Butter Idli from your order."
    assert order == {}

def test_remove_item_from_order_not_found():
    order = order_sample.copy()
    result = remove_item_from_order("Ghee Idli", order, restaurants_sample)
    assert result == "'Ghee Idli' not found in your order."
    assert order == order_sample

def test_display_menu():
    result = display_menu(restaurants_sample)
    expected_lines = [
        "=== Available Menu ===",
        "",
        "The Rameshwaram Cafe (6am – 12midnight)",
        "  Idli & Vada:",
        "    - Butter Idli ($100.00)",
        "",
        "Type an order like '1 Butter Idli' or 'list restaurants' to continue."
    ]
    assert result == "\n".join(expected_lines)

def test_display_menu_empty():
    result = display_menu({})
    assert result == "No open restaurants available to display a menu."

@patch("orders.load_state")
@patch("orders.save_state")
@patch("orders.authenticate")
@patch("orders.fetch_menu_from_api")
def test_process_order_login(mock_fetch_menu, mock_auth, mock_save, mock_load):
    mock_load.return_value = ({}, {}, False, None, None, None, None)
    mock_auth.return_value = "token123"
    mock_fetch_menu.return_value = (None, restaurants_sample)
    result = process_order("session1", "login user1 password123")
    assert "Logged in as user1. Open restaurants:" in result
    assert "The Rameshwaram Cafe" in result

@patch("orders.load_state")
def test_process_order_no_user(mock_load):
    mock_load.return_value = ({}, {}, False, None, None, None, None)
    result = process_order("session1", "list restaurants")
    assert result == "Please log in first by typing 'login <username> <password>' (e.g., 'login user1 password123')."