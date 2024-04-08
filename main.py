# app/main.py

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from app.routers.user_route import UserRouter
from app.routers.docs_route import DocsRouter
from app.settings import Settings
from app.constants.route_paths import RoutePaths
from app.routers.auth_route import AuthRouter
from app.routers.api_test_route import ApiTestRouter
from app.constants.app_constants import AppConstants
from app.base.cors_config import InitCORS

class App(RoutePaths):
    def __init__(self):
        self.app = FastAPI()
        self.settings = Settings()
        self.base_router = APIRouter(prefix=self.API_PREFIX)
        self.setup_routes()
        self.setup_static_files()
        InitCORS(app=self.app)

    def setup_static_files(self):
        self.app.mount(RoutePaths.STATIC, StaticFiles(directory="app/templates"), name=AppConstants.STATIC)
        
    def setup_routes(self):
        docs_router = DocsRouter()
        user_router = UserRouter()
        auth_router = AuthRouter()
        api_test_router = ApiTestRouter()
        self.app.include_router(user_router.router)
        self.app.include_router(docs_router.router)
        self.app.include_router(auth_router.router)
        self.app.include_router(api_test_router.router)

    def run(self):
        uvicorn.run(self.app, host=self.settings.APP_HOST, port=self.settings.APP_PORT)

if __name__ == "__main__":
    app = App()
    app.run()
