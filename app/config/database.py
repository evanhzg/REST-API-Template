from pymongo import MongoClient


def get_database():
    CONNECTION_STRING = "mongodb+srv://evan:webservices@tpwebservices-m1.autarun.mongodb.net/"

    try:
        client = MongoClient(CONNECTION_STRING)
        return client["webservices"]
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        return None


db = get_database()

if db is not None:
    print("Connected to MongoDB")
