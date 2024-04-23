from app.databases.sqlite_database_manager import SQLiteDBManager
from app.models.user_model import UserModel

class UserController(SQLiteDBManager):
    def __init__(self) -> None:
        super().__init__()
        pass
    
    def create_new_user(self, userModel: UserModel):
        print("Creating....")
        
    def get_all_users(self):
        print("All Users....")
    def get_users_by_id(self, id:str):
        print("Creating....")