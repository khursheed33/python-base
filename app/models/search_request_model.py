from pydantic import BaseModel

class SearchInEmbeddingRequestModel(BaseModel):
    user_id: str = None
    query: str
    top_results:int = 3
    collection_name: str = None
