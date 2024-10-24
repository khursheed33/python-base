from fastapi import HTTPException
from app.databases.sqlite_database_manager import SQLiteDBManager
from app.models.response_model import ResponseModel
from app.models.chat_model import ChatRequestModel

class ChatController(SQLiteDBManager):
    def __init__(self) -> None:
        super().__init__()
        pass
    
    def chat_with_llm(self, chat_model: ChatRequestModel) -> ResponseModel:
        raise HTTPException(status_code=ResponseModel.INTERNAL_SERVER_ERROR_500, detail="Unimplemented method!")