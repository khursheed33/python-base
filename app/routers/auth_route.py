from fastapi import APIRouter, HTTPException, Depends, status
from app.constants.route_paths import RoutePaths
from app.constants.route_tags import RouteTags
from app.models.auth_models import LoginModel
from app.models.response_model import ResponseModel
from app.utils.utility_manager import UtilityManager
from app.controllers.auth.auth_controller import AuthController
from app.controllers.auth.azure_ad_auth_controller import AzureADAuthController
from app.constants.app_messages import AppMessages

class AuthenticationRouter(AzureADAuthController, UtilityManager):
    def __init__(self):
        super().__init__()
        self.router = APIRouter(prefix=RoutePaths.API_PREFIX)
        self.setup_routes()

    def setup_routes(self):
        @self.router.post(RoutePaths.AUTH, tags=[RouteTags.AUTH])
        @self.catch_api_exceptions
        async def login(request: LoginModel) -> ResponseModel:
            username = request.username
            password = request.password
            if not (username or password):
                raise HTTPException(detail="Username and password required!", status_code=500)

            return await self.login_user(username=username, password=password)
        
        @self.router.put(RoutePaths.AUTH, tags=[RouteTags.AUTH])
        @self.catch_api_exceptions
        async def logout(token: str) -> ResponseModel:
            if not token:
                raise HTTPException(detail="Invalid token", status_code=500)

            return await self.logout_user(token=token)
        
        # Route with token validation
        @self.router.post("/protected-route", tags=[RouteTags.AUTH])
        @self.catch_api_exceptions
        async def protected_route(request: dict, current_user: dict = Depends(self.get_current_active_user)) -> ResponseModel:
            return ResponseModel(
                success=True,
                message="You have access to this route",
                data=[current_user, request]
            )

        # Route without token validation (will fail)
        @self.router.post("/another-protected-route", tags=[RouteTags.AUTH])
        @self.catch_api_exceptions
        async def another_protected_route(request: dict) -> ResponseModel:
            # This route does not use the token validation dependency
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is missing or invalid"
            )