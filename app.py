from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB configuration
MONGO_URI = "mongodb+srv://zahidbhaimbbs:zahidshaikhmongodb@cluster0.a5fck.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Replace with your MongoDB URI
DATABASE_NAME = "StudentMarks"
COLLECTION_NAME = "Marks"

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

@app.route('/')
def home():
    return "Welcome to the Flask-MongoDB App!"

# Fetch all records
@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    try:
        data = list(collection.find({}, {"_id": 0}))  # Exclude `_id` if not needed
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a new record
@app.route('/add-record', methods=['POST'])
def add_record():
    try:
        record = request.json  # JSON data from the client
        if not record.get("name") or not record.get("marks"):
            return jsonify({"error": "Both 'name' and 'marks' fields are required"}), 400

        inserted = collection.insert_one(record)
        return jsonify({"message": "Record added successfully", "id": str(inserted.inserted_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update marks in a record
@app.route('/update-marks/<record_id>', methods=['PUT'])
def update_marks(record_id):
    try:
        updated_data = request.json  # JSON data from the client
        new_marks = updated_data.get("marks")

        if new_marks is None:
            return jsonify({"error": "The 'marks' field is required"}), 400

        result = collection.update_one(
            {"_id": ObjectId(record_id)},
            {"$set": {"marks": new_marks}}
        )

        if result.matched_count == 0:
            return jsonify({"error": "No record found with the given ID"}), 404

        return jsonify({"message": "Marks updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a record
@app.route('/delete-record/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    try:
        result = collection.delete_one({"_id": ObjectId(record_id)})

        if result.deleted_count == 0:
            return jsonify({"error": "No record found with the given ID"}), 404

        return jsonify({"message": "Record deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
