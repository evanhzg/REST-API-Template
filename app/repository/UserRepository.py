from fastapi import HTTPException
from app.config.database import db, get_database
from faker import Faker
import datetime


# importing ObjectId from bson library
from bson.objectid import ObjectId

from app.models.User import User
from fastapi import HTTPException

# For example measures, creating fake data using Faker
# https://faker.readthedocs.io/en/master/
fake = Faker()


# ======================DATABASE========================


# Initiate the database access
db_name = "users"
db = get_database()

# Define collection / table user
# (using mongodb for this example)
collection = db[db_name]


# ========================CRUD===========================



async def add_user(user: User):
    try:
        collection.insert_one(user.dict())

        return user

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to add user: {str(e)}"
        )

async def get_all_user():
    try:
        fetched_user = collection.find({}, {"_id": 0})
        users = []
        if fetched_user:
            for user in fetched_user:
                users.append(user)
            return users
        else:
            raise HTTPException(status_code=404, detail="No user to return")

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to return user: {str(e)}"
        )


    # Second READ function : Lone user fetch
    async def get_user_by_id(id: str):
        # Fetching data with matching id, could do the same
        try:
            user = collection.find({"_id": ObjectId(id)}, {"_id": 0})

            user = list(user)

            if user:
                return user
            else:
                raise HTTPException(status_code=404, detail="User doesn't exist")

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to return user: {str(e)}"
            )
        


# Second READ function : Lone user fetch
async def get_user_by_id(id: str):
    # Fetching data with matching id, could do the same
    # for any parameter but would need {"_id": 0} to
    # contain the results
    try:
        user = collection.find({"_id": ObjectId(id)}, {"_id": 0})

        user = list(user)

        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User doesn't exist")

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to return user: {str(e)}"
        )


# CR[U]D : Editing an existing collection entry in the db
async def edit_user(id: str, updated_data: dict):
    # finds the searched entry and sets every edited data
    # to the updated one from a dict
    collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})


# CRU[D] : Removing given entry from the database
async def delete_user_by_id(id: str):
    try:
        # Explicit, innit ?
        collection.delete_one({"_id": ObjectId(id)})

    # If user is not found or can't be deleted
    # for any reason, returns an error message
    except Exception as e:
        return {"message": f"Failed to delete user: {str(e)}"}


# PLUS: Delete all entries in the collection
async def delete_all_user():
    try:
        # Use the `delete_many` method to remove all documents from the collection
        result = collection.delete_many({})

        if result.deleted_count > 0:
            return {"message": "All user has been deleted"}
        else:
            raise HTTPException(status_code=404, detail="No user to delete")

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete user: {str(e)}"
        )
