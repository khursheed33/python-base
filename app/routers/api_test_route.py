# app/routers/ping_route.py

from fastapi import APIRouter
from app.constants.route_paths import RoutePaths
from app.constants.route_tags import RouteTags

class ApiTestRouter():
    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        @self.router.get(RoutePaths.ROOT)
        async def ping():
            return {"message": "I am Alive"}
    def setup_routes(self):
        @self.router.get(RoutePaths.PING,tags=[RouteTags.PING])
        async def ping_me():
            return {"message": "I am Alive"}
