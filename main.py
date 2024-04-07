# app/main.py

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from app.routers.user_route import UserRouter
from app.routers.docs_route import DocsRouter
from app.settings import Settings
from app.routers.route_paths import RoutePaths
from app.routers.auth_route import AuthRouter
from app.constants.app_constants import AppConstants

class App(RoutePaths):
    def __init__(self):
        self.app = FastAPI()
        self.settings = Settings()
        self.base_router = APIRouter(prefix=self.API_PREFIX)
        self.setup_routes()
        self.setup_static_files()  # Call setup_static_files method

    def setup_static_files(self):
        self.app.mount(RoutePaths.STATIC, StaticFiles(directory="app/templates"), name=AppConstants.STATIC)
        
    def setup_routes(self):
        docs_router = DocsRouter()
        user_router = UserRouter()
        auth_router = AuthRouter()
        self.app.include_router(user_router.router)
        self.app.include_router(docs_router.router)
        self.app.include_router(auth_router.router)

    def run(self):
        uvicorn.run(self.app, host=self.settings.APP_HOST, port=self.settings.APP_PORT)

if __name__ == "__main__":
    app = App()
    app.run()
