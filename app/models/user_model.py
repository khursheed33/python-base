from pydantic import BaseModel

class UserModel(BaseModel):
    id: int
    username: str
    email: str
