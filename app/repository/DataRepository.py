from fastapi import HTTPException
from app.config.database import db, get_database
from faker import Faker
import datetime


# importing ObjectId from bson library
from bson.objectid import ObjectId

from app.models.Content import Content
from fastapi import HTTPException

# For example measures, creating fake data using Faker
# https://faker.readthedocs.io/en/master/
fake = Faker()


# ======================DATABASE========================


# Initiate the database access
db_name = "example_collection"
db = get_database()

# Define collection / table content
# (using mongodb for this example)
collection = db[db_name]


# ========================CRUD===========================



# [C]RUD : Add data to the db model
async def add_content(content: Content):
    try:

        # Convert the Content object to a dictionary before saving it to the database
        content_dict = content.dict()

        # import to convert a string
        content_dict["birthdate"] = datetime.datetime.combine(
            content_dict["birthdate"], datetime.time()
        )
        # Insert the content into the database and get the inserted content's id
        collection.insert_one(content_dict)

        # Return the Content object
        return content

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to add content: {str(e)}"
        )

# C[R]UD : Fetch content set in the database
# We'll get 2 of those, here is a fetch of all content
async def get_all_content():
    try:
        # Getting all of the collection content
        fetched_content = collection.find({}, {"_id": 0})

        # Define the empty table containing the object results
        all_content = []

        # Each object will be put in our table
        for content in fetched_content:
            all_content.append(Content(**content))

        if not all_content:
            raise HTTPException(status_code=404, detail="No content has been found")

        # Returns the table with all of the collection
        return all_content

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to return content: {str(e)}"
        )


# Second READ function : Lone content fetch
async def get_content_by_id(id: str):
    # Fetching data with matching id, could do the same
    # for any parameter but would need {"_id": 0} to
    # contain the results
    try:
        content = collection.find({"_id": ObjectId(id)}, {"_id": 0})

        content = list(content)

        if content:
            return content
        else:
            raise HTTPException(status_code=404, detail="Content doesn't exist")

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to return content: {str(e)}"
        )


# CR[U]D : Editing an existing collection entry in the db
async def edit_content(id: str, updated_data: dict):
    # finds the searched entry and sets every edited data
    # to the updated one from a dict
    collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})


# CRU[D] : Removing given entry from the database
async def delete_content_by_id(id: str):
    try:
        # Explicit, innit ?
        collection.delete_one({"_id": ObjectId(id)})

    # If user is not found or can't be deleted
    # for any reason, returns an error message
    except Exception as e:
        return {"message": f"Failed to delete content: {str(e)}"}


# PLUS: Delete all entries in the collection
async def delete_all_content():
    try:
        # Use the `delete_many` method to remove all documents from the collection
        result = collection.delete_many({})

        if result.deleted_count > 0:
            return {"message": "All content has been deleted"}
        else:
            raise HTTPException(status_code=404, detail="No content to delete")

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete content: {str(e)}"
        )
