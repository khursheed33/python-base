
from fastapi import FastAPI
from app.routers.test_route import TestRouter
from app.routers.user_route import UserRouter
from app.routers.docs_route import DocsRouter

class RouterRegistration:
    def __init__(self, app:FastAPI):
        docs_router = DocsRouter()
        user_router = UserRouter()
        test_router = TestRouter()
        
        app.include_router(docs_router.router)
        app.include_router(user_router.router)
        app.include_router(test_router.router)
