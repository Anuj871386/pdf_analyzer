from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

#config

SECRET = "SUPER_SECRET_KEY_CHANGE_ME"
ALGO = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Pre-generated password hash
USER = {
    "username": "admin",
    "password": "$2b$12$KIXQJH8FQ2F8eW0M0g0y.eEyx0N6oJp6GfZKxZ9H3P0QfUu7zv1bC"
}

print("USER---", USER)

def authenticate(username, password):
    return username == "admin" and password == "admin123"


def create_token():
    payload = {
        "sub": USER["username"],
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_token()
    return {
        "access_token": token,
        "token_type": "bearer"
    }

def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    # temporary user object
    return {"username": "test_user"}

