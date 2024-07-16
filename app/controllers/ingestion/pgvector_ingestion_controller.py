
from typing import List
from fastapi import UploadFile
from app.embeddings.pgvector_embedding_manager import PGVectorEmbeddings
from app.utils.utility_manager import UtilityManager
from app.models.all_models import ResponseModel

class PGVectorIngestionController(UtilityManager):
    def __init__(self) -> None:
        super().__init__()
        self.vectorstore = PGVectorEmbeddings()

    async def create_embeddings(self, files: List[UploadFile]) -> ResponseModel:
        final_collection_name = "vectorstore"
        uploaded = await self.upload(files=files)
        uploaded_dir = uploaded.get('directory')
        docs = self.load_directory(directory=uploaded_dir, chunk_size=1000, chunk_overlap=100)
        result = self.vectorstore.create_vector_embeddings(collection_name=final_collection_name, docs=docs)
        return ResponseModel(message="Uploaded",data=[result],status_code=ResponseModel.CREATED_201)
 
    async def search_in_embedding(self, input:str, top_k:int = 3, collection_name:str='vectorstore') -> ResponseModel:
        result =  self.vectorstore.search_in_vector(top_k=top_k,collection_name=collection_name, query=input)
        return ResponseModel(message="Result found",data=[{"content": result}])
    
    async def delete_collection_embeddings(self, collection_name:str='langchain') -> ResponseModel:
        response =  await self.vectorstore.delete_vector( collection_name=collection_name)
        return ResponseModel(message="Deleted Successfully!",data=[{"content": response}])