import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from app.routers.user_route import UserRouter
from app.routers.docs_route import DocsRouter
from app.settings import Settings
from app.routers.route_paths import RoutePaths

class App(RoutePaths):
    def __init__(self):
        self.app = FastAPI()
        self.settings = Settings()
        self.base_router = APIRouter(prefix=self.API_PREFIX)
        self.setup_routes()
        self.setup_static_files()

    def setup_routes(self):
        docs_router = DocsRouter()
        user_router = UserRouter()
        self.base_router.include_router(user_router.router)
        self.base_router.include_router(docs_router.router)

    def setup_static_files(self):
        self.base_router.mount("/static", StaticFiles(directory="app/templates"), name="static")

    def run(self):
        uvicorn.run(self.app, host=self.settings.APP_HOST, port=self.settings.APP_PORT)

if __name__ == "__main__":
    app = App()
    app.run()
