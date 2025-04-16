import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load MONGO_DB_URL from .env file
load_dotenv()

# Get the MongoDB connection URL
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

# Replace these with your actual database and collection names
DATABASE_NAME = "KULDEEP"
COLLECTION_NAME = "NetworkData"

def test_mongo():
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_DB_URL)
        print("✅ Connected to MongoDB!")

        # Access the database and collection
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        # Count and display number of documents
        document_count = collection.count_documents({})
        print(f"📊 Total documents in collection '{COLLECTION_NAME}': {document_count}")

        # Optionally print a few sample records
        sample_docs = collection.find().limit(5)
        print("\n📄 Sample Documents:")
        for doc in sample_docs:
            print(doc)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_mongo()
