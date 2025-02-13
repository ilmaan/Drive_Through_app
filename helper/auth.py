from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import Depends



# Constants for authentication
SECRET_KEY = "dummykey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# JWT Authentication setup for authentication

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User:
    def __init__(self, username: str, full_name: str, email: str, hashed_password: str):
        self.username = username
        self.full_name = full_name
        self.email = email
        self.hashed_password = hashed_password

# test user database
test_user = {
    "testuser": User(
        username="testuser",
        full_name="Test User",
        email="test@example.com",
        hashed_password=pwd_context.hash("password")
    )
}


# Function to verify password - ref fastapi documentation
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Function to create JWT tokene
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




