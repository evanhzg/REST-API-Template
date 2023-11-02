from pymongo import MongoClient


def get_database():
    CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.1"

    try:
        client = MongoClient(CONNECTION_STRING)
        return client["webservices"]
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        return None


db = get_database()

if db is not None:
    print("Connected to MongoDB")
