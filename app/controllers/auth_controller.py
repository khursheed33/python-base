
from jose import  jwt
from datetime import datetime, timedelta
from typing import Optional
from app.models.user_model import UserModel
from dotenv import dotenv_values



class AuthController:
    def __init__(self) -> None:
        self.config = dotenv_values(".env")


  
    def verify_password(self, plain_password, hashed_password):
        if not (plain_password or hashed_password):
            return False
        return False

    def get_user(self, email: str):
        # Mocked user data, replace this with your actual user retrieval logic
        if email == self.config.get("TEST_USER_EMAIL"):
            return UserModel(**{
                "id": 1,
                "username": "testuser",
                "email": "testuesr@gmail.com"
            })

    def authenticate_user(self, email: str, password: str):
        if not (email or password):
            return False
        return False

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.config.get('SECRET_KEY'), algorithm=self.config.get('ALGORITHM'))
        return encoded_jwt
        