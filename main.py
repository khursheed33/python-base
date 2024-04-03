from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers.user_route import UserRouter
from app.routers.docs_route import DocsRouter
from app.settings import Settings

class App:
    def __init__(self):
        self.app = FastAPI()
        self.settings = Settings()
        self.setup_routes()
        self.setup_static_files()

    def setup_routes(self):
        docs_router = DocsRouter()
        user_router = UserRouter()
        self.app.include_router(user_router.router)
        self.app.include_router(docs_router.router)

    def setup_static_files(self):
        self.app.mount("/static", StaticFiles(directory="app/templates"), name="static")

    def run(self):
        import uvicorn
        uvicorn.run(self.app, host=self.settings.APP_HOST, port=self.settings.APP_PORT)

if __name__ == "__main__":
    app = App()
    app.run()
