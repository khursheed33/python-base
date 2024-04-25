# app/routers/user_route.py

from fastapi import APIRouter, Body
from app.constants.route_paths import RoutePaths
from app.constants.route_tags import RouteTags
from typing import List
from fastapi import File, UploadFile
from app.controllers.shared.shared_controller import SharedController
from app.utils.utility_manager import UtilityManager
from app.constants.constant_manager import ConstantManager
from app.models.all_models import SearchInEmbeddingRequestModel, ResponseModel


class SharedRouter(SharedController, UtilityManager):
    def __init__(self):
        super().__init__()
        self.router = APIRouter(prefix=RoutePaths.API_PREFIX)
        self.setup_routes()

    def setup_routes(self):
        @self.router.post(RoutePaths.VECTOR_DOCS_UPLOAD, tags=[RouteTags.VECTOR_DB])
        @self.catch_api_exceptions
        async def create_document_embeddings(collection_name:str = None, user_id:str=None,files: List[UploadFile] = File(...)) -> ResponseModel:
            if user_id:
                collection_name = f'{collection_name}_{user_id}'
            return await self.create_embeddings(files=files,collection_name=collection_name)

        @self.router.post(RoutePaths.VECTOR_DOCS_SEARCH, tags=[RouteTags.VECTOR_DB])
        @self.catch_api_exceptions
        async def search_in_embeddings(request: SearchInEmbeddingRequestModel = Body(...)) -> ResponseModel:
            user_id = request.user_id if request.user_id != ConstantManager.STRING else None
            collection_name = request.collection_name if request.collection_name != ConstantManager.STRING else None
            if user_id and collection_name:
                collection_name = f'{collection_name}_{user_id}'
            input = request.query
            top_k = request.top_results
            return  await self.search_in_embedding(input=input, collection_name=collection_name, top_k=top_k)

        @self.router.delete(RoutePaths.VECTOR_DOCS, tags=[RouteTags.VECTOR_DB],description="Default Collection Name: langchain")
        @self.catch_api_exceptions
        async def delete_data_from_vector_collection(collection_name: str,user_id:str=None,) -> ResponseModel:
            if user_id:
                collection_name = f'{collection_name}_{user_id}'
            return await self.delete_collection_embeddings(collection_name=collection_name)
