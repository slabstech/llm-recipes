import unittest
from unittest.mock import patch, Mock
import json
import order_logic

class TestOrderLogic(unittest.TestCase):

    def setUp(self):
        # Mock Redis client
        self.mock_redis = Mock()
        order_logic.redis_client = self.mock_redis
        
        # Sample data
        self.restaurants = {
            "rest1": {"name": "Spice Haven", "menu": {"1": {"name": "Butter Chicken", "price": 250}}},
            "rest2": {"name": "Biryani Bliss", "menu": {"3": {"name": "Chicken Biryani", "price": 300}}}
        }
        self.order = {"rest1:1": 2}
        self.token = "mock-token"

    @patch('order_logic.requests.get')
    def test_fetch_menu_from_api_success(self, mock_get):
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"restaurants": self.restaurants}
        mock_get.return_value = mock_response
        
        error, result = order_logic.fetch_menu_from_api()
        self.assertIsNone(error)
        self.assertEqual(result, self.restaurants)

    @patch('order_logic.requests.get')
    def test_fetch_menu_from_api_failure(self, mock_get):
        # Mock failed API response
        mock_get.side_effect = order_logic.requests.RequestException("Connection error")
        
        error, result = order_logic.fetch_menu_from_api()
        self.assertTrue(error.startswith("Failed to fetch menu from API"))
        self.assertEqual(result, {})

    @patch('order_logic.requests.post')
    def test_authenticate_success(self, mock_post):
        # Mock successful login response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": self.token}
        mock_post.return_value = mock_response
        
        token = order_logic.authenticate("user1", "password123")
        self.assertEqual(token, self.token)

    @patch('order_logic.requests.post')
    def test_authenticate_failure(self, mock_post):
        # Mock failed login response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = order_logic.requests.RequestException("Invalid credentials")
        mock_post.return_value = mock_response
        
        token = order_logic.authenticate("user1", "wrongpass")
        self.assertIsNone(token)

    @patch('order_logic.requests.get')
    def test_fetch_user_credentials_from_api_success(self, mock_get):
        # Mock successful user data response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "John Doe", "address": "123 Main St", "phone": "9876543210"}
        mock_get.return_value = mock_response
        
        error, credentials = order_logic.fetch_user_credentials_from_api("user1", self.token)
        self.assertIsNone(error)
        self.assertEqual(credentials["name"], "John Doe")

    def test_is_single_restaurant_single(self):
        self.assertTrue(order_logic.is_single_restaurant(self.order))

    def test_is_single_restaurant_multiple(self):
        mixed_order = {"rest1:1": 2, "rest2:3": 1}
        self.assertFalse(order_logic.is_single_restaurant(mixed_order))

    def test_generate_order_summary(self):
        summary = order_logic.generate_order_summary(self.order, self.restaurants)
        expected = "=== Current Order ===\nButter Chicken x2 (from Spice Haven) - ₹500\nTotal: ₹500"
        self.assertEqual(summary, expected)

    def test_generate_order_summary_empty(self):
        summary = order_logic.generate_order_summary({}, self.restaurants)
        self.assertEqual(summary, "No items in your order.")

    def test_remove_item_from_order_success(self):
        order_copy = self.order.copy()
        feedback = order_logic.remove_item_from_order("Butter Chicken", order_copy, self.restaurants)
        self.assertEqual(feedback, "Removed Butter Chicken from your order.")
        self.assertEqual(order_copy, {})

    def test_remove_item_from_order_not_found(self):
        feedback = order_logic.remove_item_from_order("Pizza", self.order, self.restaurants)
        self.assertEqual(feedback, "'pizza' not found in your order.")

    @patch('order_logic.client.chat.complete')
    def test_parse_and_search_order_success(self, mock_chat):
        # Mock Mistral API response
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='[{"item": "Butter Chicken", "quantity": 2}]'))]
        mock_chat.return_value = mock_response
        
        feedback, new_order = order_logic.parse_and_search_order("I want 2 butter chickens", self.restaurants)
        self.assertEqual(feedback, "Added 2 x Butter Chicken (from Spice Haven) to your order.")
        self.assertEqual(new_order, {"rest1:1": 2})

    @patch('order_logic.client.chat.complete')
    def test_parse_and_search_order_invalid(self, mock_chat):
        # Mock invalid Mistral API response
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"error": "Invalid input"}'))]
        mock_chat.return_value = mock_response
        
        feedback, new_order = order_logic.parse_and_search_order("invalid", self.restaurants)
        self.assertEqual(feedback, "Invalid input")
        self.assertEqual(new_order, {})

if __name__ == "__main__":
    unittest.main()