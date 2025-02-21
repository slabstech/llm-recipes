from flask import Flask, jsonify

app = Flask(__name__)

# Mock data with multiple restaurants
RESTAURANTS = {
    "rest1": {
        "name": "Spice Haven",
        "menu": {
            "1": {"name": "Butter Chicken", "price": 250},
            "2": {"name": "Paneer Tikka", "price": 200}
        }
    },
    "rest2": {
        "name": "Biryani Bliss",
        "menu": {
            "3": {"name": "Chicken Biryani", "price": 300},
            "4": {"name": "Veg Biryani", "price": 220}
        }
    },
    "rest3": {
        "name": "Pizza Palace",
        "menu": {
            "5": {"name": "Veg Pizza", "price": 350},
            "6": {"name": "Pepperoni Pizza", "price": 400}
        }
    }
}

# Mock Menu API endpoint - returns all restaurants and their menus
@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify({"restaurants": RESTAURANTS})

# Mock Users API endpoint
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    if user_id == "user1":
        return jsonify({
            "name": "John Doe",
            "address": "123 Main St, Delhi",
            "phone": "9876543210"
        })
    return jsonify({}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)