from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = "mongodb+srv://zahidbhaimbbs:zahidshaikhmongodb@cluster0.a5fck.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Replace with your MongoDB connection string
DB_NAME = "instagram"           # Replace with your database name
COLLECTION_NAME = "profile" # Replace with your collection name

# Initialize MongoDB Client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route('/profiles', methods=['GET'])
def get_profiles():
    try:
        # Fetch all documents from the collection
        profiles = list(collection.find({}, {"_id": 0}))  # Exclude the `_id` field
        return jsonify(profiles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
