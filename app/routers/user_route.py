# app/routers/user_route.py

from fastapi import APIRouter
from app.models.user_model import UserModel
from app.constants.route_paths import RoutePaths
from app.constants.route_tags import RouteTags

class UserRouter():
    def __init__(self):
        self.router = APIRouter(prefix=RoutePaths.API_PREFIX)
        self.setup_routes()

    def setup_routes(self):
        @self.router.get(RoutePaths.USERS, tags=[RouteTags.USERS])  # Update the path to include the prefix
        async def read_users():
            return [{"username": "Rick"}, {"username": "Morty"}]
        
        @self.router.post(RoutePaths.USERS, tags=[RouteTags.USERS])  # Update the path to include the prefix
        async def create_user(user: UserModel):
            return user
