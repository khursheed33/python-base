from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.utils.error_logger import error_logging
from app.routers.route_paths import RoutePaths

class DocsRouter(RoutePaths):
    def __init__(self):
        self.router = APIRouter(prefix=self.API_PREFIX)
        self.templates = Jinja2Templates(directory="app/templates")
        self.setup_routes()

    @error_logging
    def setup_routes(self):
        @self.router.get(self.DOCS, response_class=HTMLResponse, include_in_schema=False, tags=['docs'])  
        async def custom_swagger_ui_html(request: Request):
            """
            Custom route to serve Swagger UI HTML.
            """
            return self.templates.TemplateResponse("swagger_ui.html", {"request": request})

        # Instead of including the function directly, include the router itself
        self.router.include_router(
            self.router,
            tags=["Custom Swagger UI"],
        )
