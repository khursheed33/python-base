from pydantic import BaseModel
from typing import List
from app.utils.get_current_timestamp import get_current_timestamp_str

class APICallStatus:
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'

class StatusCodes:
    INTERNAL_SERVER_ERROR_500 = 500
    NOT_FOUND_404 = 404
    NOT_ALLOWED_400 = 400
    BAD_RESQUEST_403 = 303
    OK_200 = 200
    CREATED_201 = 201
class ResponseModel(BaseModel, APICallStatus, StatusCodes):
    status:str = APICallStatus.SUCCESS
    error:str = None
    status_code:int = StatusCodes.OK_200
    message:str
    data: List = []
    timestamp: str = get_current_timestamp_str()