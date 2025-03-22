
from bson import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient
import bcrypt
import jwt
import datetime
from constant import MONGO_URI, SECRET_KEY
app = Flask(__name__)


client = MongoClient(MONGO_URI)
db = client["test-db"]

user_collection=db["user"]
login_collection = db["login"]



# Insert a user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    name = data.get("name")
    age = data.get("age")

    if not name or not age:
        return jsonify({"error": "Name and age are required"}), 400

    user_id = user_collection.insert_one({"name": name, "age": age}).inserted_id
    return jsonify({"message": "User added", "id": str(user_id)}), 201

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = list(user_collection.find({}, {"_id": 1, "name": 1, "age": 1}))
    for user in users:
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
    return jsonify(users)

# Get user by ID
@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_collection.find_one({"_id": ObjectId(user_id)}, {"_id": 1, "name": 1, "age": 1})
    if user:
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# Update a user
@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    name = data.get("name")
    age = data.get("age")

    if not name or not age:
        return jsonify({"error": "Name and age are required"}), 400

    result = user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"name": name, "age": age}})
    
    if result.matched_count:
        return jsonify({"message": "User updated"}), 200
    return jsonify({"error": "User not found"}), 404

# Delete a user
@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = user_collection.delete_one({"_id": ObjectId(user_id)})
    
    if result.deleted_count:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404
# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check if user exists with the provided email and password
    user = login_collection.find_one({"email": email, "password": password})

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)
