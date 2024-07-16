# app/main.py

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from app.base.settings import Settings
from app.constants.route_paths import RoutePaths
from app.constants.app_constants import AppConstants
from app.base.router_registration import RouterRegistration
from app.base.cors_config import InitCORS
from app.constants.fast_api_constants import FastAPIConstants
from app.constants.directory_names import DirectoryNames

class App(RoutePaths):
    def __init__(self):
        self.app = FastAPI(
            title=FastAPIConstants.TITLE,
            description=FastAPIConstants.DESCRIPTION,
            summary=FastAPIConstants.SUMMARY,
            version=FastAPIConstants.VERSION,
            terms_of_service=FastAPIConstants.T_N_C,
            contact=FastAPIConstants.CONTACT,
            license_info=FastAPIConstants.LICENSE_INFO,
            openapi_tags=FastAPIConstants.OPENAPI_TAGS_METADATA,
        )
        self.settings = Settings()
        self.base_router = APIRouter(prefix=self.API_PREFIX)
        self.setup_routes()
        self.setup_static_files()
        InitCORS(app=self.app)

    def setup_static_files(self):
        self.app.mount(RoutePaths.STATIC, StaticFiles(
            directory=DirectoryNames.TEMPLATES), name=AppConstants.STATIC)

    def setup_routes(self):
        RouterRegistration(app=self.app)

    def run(self):
        uvicorn.run(self.app, host=self.settings.APP_HOST,
                    port=self.settings.APP_PORT)


if __name__ == "__main__":
    app = App()
    app.run()
