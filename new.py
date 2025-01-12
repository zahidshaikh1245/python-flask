from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = "mongodb+srv://zahidbhaimbbs:zahidshaikhmongodb@cluster0.a5fck.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Replace with your MongoDB connection string
DB_NAME = "instagram"           # Replace with your database name
COLLECTION_NAME = "profile"     # Replace with your collection name

# Initialize MongoDB Client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# GET API to fetch profiles
@app.route('/profiles', methods=['GET'])
def get_profiles():
    try:
        profiles = list(collection.find({}, {"_id": 0}))  # Exclude the `_id` field
        return jsonify(profiles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST API to add a new profile
@app.route('/profiles', methods=['POST'])
def add_profile():
    try:
        new_profile = request.get_json()

        if not new_profile:
            return jsonify({"error": "Request body must be JSON"}), 400

        required_fields = ["name", "username", "followers", "following", "bio"]
        missing_fields = [field for field in required_fields if field not in new_profile]

        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        result = collection.insert_one(new_profile)
        return jsonify({"message": "Profile added successfully", "inserted_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PUT API to update an existing profile
@app.route('/profiles/<string:username>', methods=['PUT'])
def update_profile(username):
    try:
        updated_data = request.get_json()

        if not updated_data:
            return jsonify({"error": "Request body must be JSON"}), 400

        result = collection.update_one(
            {"username": username},
            {"$set": updated_data}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Profile not found"}), 404

        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE API to delete a profile
@app.route('/profiles/<string:username>', methods=['DELETE'])
def delete_profile(username):
    try:
        result = collection.delete_one({"username": username})

        if result.deleted_count == 0:
            return jsonify({"error": "Profile not found"}), 404

        return jsonify({"message": "Profile deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
