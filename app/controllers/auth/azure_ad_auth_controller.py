from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import requests
from app.models.response_model import ResponseModel
from app.utils.utility_manager import UtilityManager
from app.enums.env_keys import EnvKeys

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AzureADAuthController(UtilityManager):
    def __init__(self) -> None:
        super().__init__()
        self.__tenant_id = self.get_env_variable(EnvKeys.AZURE_AD_TENANT_ID.value)
        self.__client_id = self.get_env_variable(EnvKeys.AZURE_AD_CLIENT_ID.value)
        self.__client_secret = self.get_env_variable(EnvKeys.AZURE_AD_CLIENT_SECRET.value)
        self.__authority = f"https://login.microsoftonline.com/{self.__tenant_id}"
        self.__token_url = f"{self.__authority}/oauth2/v2.0/token"
        self.__userinfo_url = "https://graph.microsoft.com/oidc/userinfo"

    async def login_user(self, username: str, password: str) -> ResponseModel:
        try:
            data = {
                'client_id': self.__client_id,
                'scope': 'openid profile offline_access',
                'username': username,
                'password': password,
                'grant_type': 'password',
                'client_secret': self.__client_secret
            }
            response = requests.post(self.__token_url, data=data)
            response.raise_for_status()
            token = response.json()
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
        # Azure AD does not provide a direct logout endpoint, you should handle logout on the client-side
        return ResponseModel(
            message="Logged out"
        )

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> dict:
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(self.__userinfo_url, headers=headers)
            response.raise_for_status()
            user_info = response.json()
            return user_info
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )

    async def get_current_active_user(self, token: str = Depends(oauth2_scheme)) -> dict:
        user = await self.get_current_user(token)
        return user
