
from fastapi import FastAPI
from app.routers.test_route import TestRouter
from app.routers.chat_route import ChatRouter
from app.routers.docs_route import DocsRouter

class RouterRegistration:
    def __init__(self, app:FastAPI):
        docs_router = DocsRouter()
        chat_router = ChatRouter()
        test_router = TestRouter()
        
        app.include_router(docs_router.router)
        app.include_router(chat_router.router)
        app.include_router(test_router.router)
