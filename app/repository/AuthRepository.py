from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from app.config.database import get_database

from app.models.User import User
from app.repository.UserRepository import get_user_by_username

db = get_database()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
# This is the secret key used to encode and decode JWTs.
SECRET_KEY = "secret"

# This is the algorithm used to encode and decode JWTs.
ALGORITHM = "HS256"

# Create an instance of the UserRepository


async def encode_jwt(user: User) -> str:
    payload = {
        "sub": user.username,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, "secret", algorithm="HS256")
    db.tokens.insert_one({"username": user.username, "token": token})
    return token

# This is the URL where the client will send the username and password to get a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# This function decodes a JWT and gets the current user.
async def get_current_user(token: str = Depends(oauth2_scheme)):    
    try:
        # Decode the JWT
        payload = jwt.decode(token, "secret", algorithms=[ALGORITHM])
        
        # Get the user from the database
        user = await get_user_by_username(payload["sub"])
        # Check if the user's token matches the provided token
        if db["tokens"].find_one({"username": payload["sub"]})["token"] != token:         
            raise credentials_exception
        
        return user
    except jwt.JWTError:
        raise credentials_exception
