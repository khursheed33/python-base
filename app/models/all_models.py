from app.models.search_request_model import SearchInEmbeddingRequestModel
from app.models.user_model import UserModel
from app.models.response_model import ResponseModel

class AllModels(SearchInEmbeddingRequestModel,UserModel, ResponseModel):
    def __init__(self) -> None:
        super().__init__()