from fastapi import APIRouter, Depends, HTTPException, status

from app.repository.AuthRepository import User, get_current_user

app = APIRouter()

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    print("oui")
    
    return current_user