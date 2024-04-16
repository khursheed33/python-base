from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.utils.error_logger import error_logging
from app.routers.route_paths import RoutePaths
from app.routers.route_tags import RouteTags

class DocsRouter():
    def __init__(self):
        self.router = APIRouter(prefix=RoutePaths.API_PREFIX)
        self.templates = Jinja2Templates(directory="app/templates")
        self.setup_routes()

    def setup_routes(self):
        @self.router.get(RoutePaths.DOCS, response_class=HTMLResponse, include_in_schema=False, tags=[RouteTags.DOCS])  
        async def custom_swagger_ui_html(request: Request):
            """
            Custom route to serve Swagger UI HTML.
            """
            return self.templates.TemplateResponse("swagger_ui.html", {"request": request})
