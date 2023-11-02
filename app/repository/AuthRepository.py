from fastapi import Depends, HTTPException, status
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

from app.models.User import User

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
# This is the secret key used to encode and decode JWTs.
SECRET_KEY = "secret"

# This is the algorithm used to encode and decode JWTs.
ALGORITHM = "HS256"

def encode_jwt(user: User):
    payload = {
        "sub": user.username,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# This is the URL where the client will send the username and password to get a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# This function decodes a JWT and gets the current user.
async def get_current_user(token: str = Depends(oauth2_scheme)):    
    try:
        # Decode the JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Ignore the 'sub' claim in the payload and always return a predefined user
        user = User(username="johndoe", email="johndoe@example.com", disabled=False)
        return user
    except jwt.JWTError:
        raise credentials_exception
