from pydantic import BaseModel
from typing import List
from app.utils.get_current_timestamp import get_current_timestamp_str
from app.constants.constant_manager import APICallStatus
class ResponseModel(BaseModel):
    status:str = APICallStatus.SUCCESS
    error:str = None
    status_code:int = 200
    message:str
    data: List = []
    timestamp: str = get_current_timestamp_str()