# app/routers/user_route.py

from fastapi import APIRouter
from app.models.user_model import UserModel
from app.routers.route_paths import RoutePaths

class UserRouter(RoutePaths):
    def __init__(self):
        self.router = APIRouter(prefix=self.API_PREFIX)
        self.setup_routes()

    def setup_routes(self):
        @self.router.get(self.USERS, tags=["users"])  # Update the path to include the prefix
        async def read_users():
            return [{"username": "Rick"}, {"username": "Morty"}]
        
        @self.router.post(self.USERS, tags=["users"])  # Update the path to include the prefix
        async def create_user(user: UserModel):
            return user
