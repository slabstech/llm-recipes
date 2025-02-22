from flask import Flask, jsonify, request
import jwt
import datetime

app = Flask(__name__)

# Mock data with multiple restaurants
RESTAURANTS = {
    "rest1": {"name": "Spice Haven", "menu": {"1": {"name": "Butter Chicken", "price": 250}, "2": {"name": "Paneer Tikka", "price": 200}}},
    "rest2": {"name": "Biryani Bliss", "menu": {"3": {"name": "Chicken Biryani", "price": 300}, "4": {"name": "Veg Biryani", "price": 220}}},
    "rest3": {"name": "Pizza Palace", "menu": {"5": {"name": "Veg Pizza", "price": 350}, "6": {"name": "Pepperoni Pizza", "price": 400}}}
}

# Mock user data (multiple users)
USERS = {
    "user1": {"name": "John Doe", "address": "123 Main St, Delhi", "phone": "9876543210", "password": "password123"},
    "user2": {"name": "Jane Smith", "address": "456 Elm St, Mumbai", "phone": "1234567890", "password": "securepass456"}
}

# Secret key for JWT (replace with a secure key in production)
SECRET_KEY = "your-secret-key"

# Mock Menu API endpoint
@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify({"restaurants": RESTAURANTS})

# Mock Login endpoint (OAuth2-like token issuance)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if username in USERS and USERS[username]["password"] == password:
        token = jwt.encode({
            "user_id": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({"access_token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Mock Users API endpoint with token authentication
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if payload["user_id"] == user_id and user_id in USERS:
            user_data = {k: v for k, v in USERS[user_id].items() if k != "password"}
            return jsonify(user_data)
        return jsonify({"error": "Unauthorized or user not found"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7861)