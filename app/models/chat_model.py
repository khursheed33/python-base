from pydantic import BaseModel, Field


class ChatRequestModel(BaseModel):
    question:str = Field(default="Type your question here...")
    user_id:str = Field(default=None)
    store: bool = Field(default=False)
    return_history: bool = Field(default=False)