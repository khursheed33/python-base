from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.utils.error_logger import error_logging

class DocsRouter:
    def __init__(self):
        self.router = APIRouter()
        self.templates = Jinja2Templates(directory="app/templates")
        self.setup_routes()

    @error_logging
    def setup_routes(self):
        @self.router.get("/docs", response_class=HTMLResponse, include_in_schema=False)
        async def custom_swagger_ui_html(request: Request):
            """
            Custom route to serve Swagger UI HTML.
            """
            return self.templates.TemplateResponse("swagger_ui.html", {"request": request})

        # Add the custom_swagger_ui_html route to the router
        self.router.include_router(
            custom_swagger_ui_html,
            tags=["Custom Swagger UI"],
        )
