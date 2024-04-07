from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from datetime import  timedelta

from app.models.user_model import UserModel
from dotenv import dotenv_values
from app.routers.route_paths import RoutePaths
from app.routers.route_tags import RouteTags
from app.controllers.auth_controller import AuthController

config = dotenv_values(".env")


class AuthRouter(AuthController):
    def __init__(self):
        self.router = APIRouter(prefix=RoutePaths.API_PREFIX)
        self.pwd_context = CryptContext(schemes=["bcrypt"])
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
        self.SECRET_KEY = config.get("SECRET_KEY", "your_secret_key_here")
        self.ALGORITHM = config.get("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
        self.setup_routes()
        
      
    def setup_routes(cls):
        @cls.router.get(RoutePaths.AUTH, tags=[RouteTags.AUTH])
        async def login_user(self, form_data: OAuth2PasswordRequestForm = Depends()):
            user = cls.authenticate_user(form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            access_token_expires = timedelta(minutes=config.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
            access_token = cls.create_access_token(
                data={"sub": user.email}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}

        @cls.router.post(RoutePaths.AUTH, tags=[RouteTags.AUTH])
        async def signup(self, user: UserModel):
            # Hash the password before saving it
            hashed_password ='self.pwd_context.hash(user.password)'
            user_dict = user.model_dump()
            user_dict["hashed_password"] = hashed_password
            # Here you would typically save the user to your database instead of using a mock database
            return UserModel(**user_dict)




