from app.models.search_request_model import SearchInEmbeddingRequestModel
from app.models.user_model import UserModel

class AllModels(SearchInEmbeddingRequestModel,UserModel):
    def __init__(self) -> None:
        super().__init__()