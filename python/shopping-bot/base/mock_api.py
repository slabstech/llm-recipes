from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify({
        "menu": {
            "1": {"name": "Butter Chicken", "price": 250},
            "2": {"name": "Paneer Tikka", "price": 200},
            "3": {"name": "Chicken Biryani", "price": 300},
            "4": {"name": "Veg Pizza", "price": 350}
        }
    })

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
    app.run(port=5000)