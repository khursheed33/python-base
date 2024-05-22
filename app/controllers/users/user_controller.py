from app.databases.sqlite_database_manager import SQLiteDBManager
from app.models.all_models import UserModel, ResponseModel

class UserController(SQLiteDBManager):
    def __init__(self) -> None:
        super().__init__()
        pass
    
    def create_new_user(self, userModel: UserModel) -> ResponseModel:
        return ResponseModel(message="It's a dummy message after creating user")
        
    def get_all_users(self):
        return ResponseModel(message="It's a dummy message get all users")
    def get_users_by_id(self, id:str):
        return ResponseModel(message="It's a dummy message get user by id")