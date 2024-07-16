from fastapi import APIRouter, Body, HTTPException
from app.constants.route_paths import RoutePaths
from app.constants.route_tags import RouteTags
from typing import List
from fastapi import File, UploadFile
from app.controllers.ingestion.pgvector_ingestion_controller import PGVectorIngestionController
from app.utils.utility_manager import UtilityManager
from app.constants.constant_manager import ConstantManager
from app.models.all_models import SearchInEmbeddingRequestModel, ResponseModel


class PGVectorIngestionRouter(PGVectorIngestionController, UtilityManager):
    def __init__(self):
        super().__init__()
        self.router = APIRouter(prefix=RoutePaths.API_PREFIX)
        self.setup_routes()

    def setup_routes(self):
        @self.router.post(RoutePaths.INGEST, tags=[RouteTags.INGESTION])
        @self.catch_api_exceptions
        async def create_document_embeddings(files: List[UploadFile] = File(...)) -> ResponseModel:
            return await self.create_embeddings(files=files)

        @self.router.post(RoutePaths.INGEST_SEARCH, tags=[RouteTags.INGESTION])
        @self.catch_api_exceptions
        async def search_in_embeddings(request: SearchInEmbeddingRequestModel = Body(...)) -> ResponseModel:
            if not request.user_id:
                raise HTTPException(status_code=ResponseModel.INTERNAL_SERVER_ERROR_500, detail="The user_id is required!")
                
            input = request.query
            top_k = request.top_results
            return  await self.search_in_embedding(input=input, top_k=top_k)

        @self.router.delete(RoutePaths.INGEST, tags=[RouteTags.INGESTION],description="Default Collection Name: vectorstore")
        @self.catch_api_exceptions
        async def delete_data_from_vector_collection(collection_name: str,user_id:str=None,) -> ResponseModel:
            raise HTTPException(detail="Unimplemented!",status_code=ResponseModel.BAD_RESQUEST_403)