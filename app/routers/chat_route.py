# app/routers/user_route.py

from fastapi import APIRouter
from app.models.chat_model import ChatRequestModel
from app.constants.route_paths import RoutePaths
from app.constants.route_tags import RouteTags
from app.controllers.chat.chat_controller import ChatController

class ChatRouter(ChatController):
    def __init__(self):
        super().__init__()
        self.router = APIRouter(prefix=RoutePaths.API_PREFIX)
        self.setup_routes()

    def setup_routes(self):
        @self.router.get(RoutePaths.USERS, tags=[RouteTags.USERS])
        @self.catch_api_exceptions
        async def chat(chat_model: ChatRequestModel):
            return self.chat_with_llm(chat_model=chat_model)
        
    