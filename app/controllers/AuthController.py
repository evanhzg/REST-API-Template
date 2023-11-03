from fastapi import APIRouter, Depends, HTTPException, status
from app.repository.AuthRepository import User, get_current_user, encode_jwt
from app.controllers.UserController import post_create_user_endpoint

app = APIRouter()

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    print("oui")
    return current_user

@app.post("/users/register")
async def register(user: User):
    # Call the create_user function from UserController to create the user
    created_user = await post_create_user_endpoint(user)
    
    # If the user was created successfully, return a JWT token
    if created_user:
        token = await encode_jwt(created_user)
        return {"token": token}
    else:
        raise HTTPException(status_code=400, detail="Could not create user")

@app.post("/users/login")
async def login(user: User):
    # For simplicity, this example assumes that if a user can be found, they are authenticated
    # In a real application, you should check the user's password here
    current_user = await get_current_user(user.username)
    if current_user:
        token = encode_jwt(current_user)
        return {"token": token}
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")

@app.post("/users/logout")
async def logout(current_user: User = Depends(get_current_user)):
    # For simplicity, this example doesn't actually do anything when a user logs out
    # In a real application, you might want to invalidate the user's token here
    return {"detail": "Logged out"}