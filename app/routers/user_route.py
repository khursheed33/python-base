from fastapi import APIRouter
from app.models.user_model import UserModel
from app.routers.route_paths import RoutePaths

class UserRouter(RoutePaths):
    def __init__(self):
        self.router = APIRouter(prefix=self.USERS)
        self.setup_routes()

    def setup_routes(self):
        @self.router.get("/")
        async def read_users():
            return [{"username": "Rick"}, {"username": "Morty"}]
        
        @self.router.post("/")
        async def create_user(user: UserModel):
            return user
