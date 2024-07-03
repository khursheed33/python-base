from fastapi.security import OAuth2PasswordBearer
from app.models.response_model import ResponseModel
from app.utils.utility_manager import UtilityManager
from app.enums.env_keys import EnvKeys
from app.constants.app_messages import AppMessages
from keycloak import KeycloakError, KeycloakOpenID
from fastapi import Depends, HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class AuthController(UtilityManager):
    def __init__(self) -> None:
        super().__init__()
        self.__server_url = self.get_env_variable(EnvKeys.KEYCLOACK_BASE_URL.value)
        self.__realm_name = self.get_env_variable(EnvKeys.KEYCLOACK_REALM_NAME.value)
        self.__client_id = self.get_env_variable(EnvKeys.KEYCLOACK_CLIENT_ID.value)
        # self.__client_secret = self.get_env_variable(EnvKeys.KEYCLOACK_CLIENT_SECRET.value)

        self.keycloak_openid = KeycloakOpenID(
            server_url=self.__server_url,
            client_id=self.__client_id,
            realm_name=self.__realm_name,
        )

    async def login_user(self, username: str, password: str) -> ResponseModel:
        try:
            token = self.keycloak_openid.token(username, password)
            return ResponseModel(
                message="Logged In!",
                data=[token]
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )

    async def logout_user(self, token: str) -> ResponseModel:
        try:
            self.keycloak_openid.logout(token)
            return ResponseModel(
                message="Logged out"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
            
    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> dict:
        try:
            user_info = self.keycloak_openid.userinfo(token)
            if not user_info:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials"
                )
            return user_info
        except KeycloakError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )

    async def get_current_active_user(self, token: str = Depends(oauth2_scheme)) -> dict:
        user = await self.get_current_user(token)
        # Add your role check logic here if needed
        return user
