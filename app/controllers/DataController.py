from typing import List
from fastapi import APIRouter, HTTPException
from ..models.Content import Content  # import the Profile model

from app.repository.DataRepository import (
    add_content,
    delete_all_content,
    delete_content_by_id,
    edit_content,
    get_all_content,
    get_content_by_id,
)

app = APIRouter()

# ======================ENDPOINTS=====================


# API endpoint to add to database
# Define the route, it will be the URL handling this data
# Also define the HTTP request. POST as we send data.
@app.post("/api/content/create", response_model=Content)
async def post_create_content_endpoint(content: Content):
    try:
        # Async call of Repository function, data fetching
        # ain't instantaneous and could lead to issues
        created_content = await add_content(content)

        return created_content

    # Catch specific exceptions as needed
    except Exception as e:
        return {"message": f"Failed to create content: {str(e)}"}

# API endpoint returning all content from the collection
# HTTP GET method used here as we don't send data
@app.get("/api/content", response_model=List[Content])
async def get_all_content_endpoint():
    try:
        all_content = await get_all_content()

        return all_content

    except Exception as e:
        return {"message": f"Failed to fetch content: {str(e.detail)}"}


# API endpoint returning a single entry from the collection
@app.get("/api/content/{content_id}", response_model=List[Content])
async def get_content_by_id_endpoint(content_id: str):
    try:
        # Assuming 'get_content_by_id' is a function to fetch content by '_id'
        content = await get_content_by_id(content_id)
        if content is not None:
            return content
        else:
            raise HTTPException(status_code=404, detail="Content not found")

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to return content: {str(e)}"
        )


# API endpoint to edit a given collection entry
# HTTP PUT method so we send data to an existing entry
@app.put("/api/content/{content_id}/edit")
async def put_edit_content_endpoint(content_id: str, updated_data: dict):
    try:
        await edit_content(content_id, updated_data)
        return {"message": "Content edited successfully"}

    except Exception as e:
        return {"message": f"Failed to edit content: {str(e)}"}


# API endpoint to delete a given collection entry
# HTTP DELETE method to remove given content
@app.delete("/api/content/{content_id}/delete")
async def delete_content_endpoint(content_id: str):
    try:
        await delete_content_by_id(content_id)
        return {"message": "Content deleted successfully"}

    except Exception as e:
        return {"message": f"Failed to delete content: {str(e)}"}


# API endpoint to delete every entry in the collection
@app.delete("/api/content/delete_all")
async def delete_all_content_endpoint():
    try:
        await delete_all_content()
        return {"message": "Collection successfully cleared."}

    except Exception as e:
        return {"message": f"Failed to delete content: {str(e)}"}
