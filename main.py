# app/main.py

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from app.settings import Settings
from app.routers.route_paths import RoutePaths
from app.constants.app_constants import AppConstants
from app.base.router_registration import RouterRegistration

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
        RouterRegistration(app=self.app)

    def run(self):
        uvicorn.run(self.app, host=self.settings.APP_HOST, port=self.settings.APP_PORT)

if __name__ == "__main__":
    app = App()
    app.run()
