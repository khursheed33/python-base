# app/routers/user_route.py

from fastapi import APIRouter
from app.models.user_model import UserModel
from app.constants.route_paths import RoutePaths
from app.constants.route_tags import RouteTags
from app.controllers.users.user_controller import UserController

class UserRouter(UserController):
    def __init__(self):
        super().__init__()
        self.router = APIRouter(prefix=RoutePaths.API_PREFIX)
        self.setup_routes()

    def setup_routes(self):
        @self.router.get(RoutePaths.USERS, tags=[RouteTags.USERS])  # Update the path to include the prefix
        async def get_all_useres():
            return self.get_all_users()
        
        @self.router.post(RoutePaths.USERS, tags=[RouteTags.USERS])  # Update the path to include the prefix
        async def create_new_user(user: UserModel):
            return self.create_new_user(userModel=user)
