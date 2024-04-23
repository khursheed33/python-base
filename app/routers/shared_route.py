# app/routers/user_route.py

from fastapi import APIRouter,Body
from app.constants.route_paths import RoutePaths
from app.constants.route_tags import RouteTags
from typing import List
from fastapi import File, UploadFile
from app.controllers.shared.shared_controller import SharedController
from app.utils.utility_manager import UtilityManager
from app.enums.env_keys import EnvKeys
from app.models.all_models import SearchInEmbeddingRequestModel

class SharedRouter(SharedController,UtilityManager):
    def __init__(self):
        super().__init__()
        self.router = APIRouter(prefix=RoutePaths.API_PREFIX)
        self.setup_routes()
        

    def setup_routes(self):
        @self.router.post(RoutePaths.DOCS_UPLOAD, tags=[RouteTags.VECTOR_DB])
        @self.catch_api_exceptions
        async def create_document_embeddings(files: List[UploadFile] = File(...)):
            return  self.create_embeddings(files=files)
        
        @self.router.post(RoutePaths.DOCS_SEARCH, tags=[RouteTags.VECTOR_DB]) 
        @self.catch_api_exceptions
        async def search_in_embeddings( request: SearchInEmbeddingRequestModel = Body(...)):
            user_id = request.user_id if request.user_id != "string" else None
            input = request.query
            collection_name = request.collection_name if request.collection_name != "string" else None
            top_k = request.top_results
            return self.search_in_embedding(input=input, collection_name=collection_name,top_k=top_k)
