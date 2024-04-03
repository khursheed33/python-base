from fastapi import APIRouter
from app.models.user_model import UserModel
class UserRouter:
    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        @self.router.get("/")
        async def read_users():
            return [{"username": "Rick"}, {"username": "Morty"}]
        
        @self.router.post("/", response_model=UserModel)
        async def create_user(user: UserModel):
            return user