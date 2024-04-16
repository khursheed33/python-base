# app/routers/user_route.py

from fastapi import APIRouter
from app.models.user_model import UserModel
from app.routers.route_paths import RoutePaths
from app.routers.route_tags import RouteTags

class TestRouter():
    def __init__(self):
        self.router = APIRouter(prefix=RoutePaths.API_PREFIX)
        self.setup_routes()

    def setup_routes(self):
        @self.router.get(RoutePaths.TESTS, tags=[RouteTags.TESTS])  # Update the path to include the prefix
        async def tests():
            return {"score": 85, "total_files": 12, "code_count": 1233}
