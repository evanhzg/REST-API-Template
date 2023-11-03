from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.repository.AuthRepository import get_current_user
from ..models.User import User

from app.repository.UserRepository import (
    add_user,
    delete_all_user,
    delete_user_by_id,
    edit_user,
    get_all_user,
    get_user_by_id,
)

app = APIRouter()

@app.post("/api/users/create", response_model=User)
async def post_create_user_endpoint(user: User):
    try:
        created_user = await add_user(user)
        return created_user

    except Exception as e:
        return {"message": f"Failed to create user: {str(e.detail)}"}


@app.get("/api/users", response_model=List[User])
async def get_all_user_endpoint():
    try:
        all_user = await get_all_user()

        return all_user

    except Exception as e:
        return {"message": f"Failed to fetch user: {str(e.detail)}"}


@app.get("/api/users/{user_id}", response_model=List[User])
async def get_user_by_id_endpoint(user_id: str):
    try:
        user = await get_user_by_id(user_id)
        if user is not None:
            return user
        else:
            raise HTTPException(status_code=404, detail="user not found")

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to return user: {str(e)}"
        )


@app.put("/api/users/{user_id}/edit")
async def put_edit_user_endpoint(user_id: str, updated_data: dict):
    try:
        await edit_user(user_id, updated_data)
        return {"message": "user edited successfully"}

    except Exception as e:
        return {"message": f"Failed to edit user: {str(e.detail)}"}


@app.delete("/api/users/{user_id}/delete", dependencies=[Depends(get_current_user)])
async def delete_user_endpoint(user_id: str):
    try:
        await delete_user_by_id(user_id)
        return {"message": "user deleted successfully"}

    except Exception as e:
        return {"message": f"Failed to delete user: {str(e)}"}


@app.delete("/api/users/delete_all", dependencies=[Depends(get_current_user)])
async def delete_all_user_endpoint():
    try:
        await delete_all_user()
        return {"message": "Collection successfully cleared."}

    except Exception as e:
        return {"message": f"Failed to delete user: {str(e)}"}
