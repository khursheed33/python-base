
import shutil
from typing import List
from fastapi import UploadFile,Body
from app.embeddings.pgvector_embeddings import PGVectorEmbeddings
from app.llm.azure_openai_rag import AzureOpenAIRAG
from app.utils.utility_manager import UtilityManager
from app.llm.local_embeddings import ChromaVectorStoreWithLocalEmbeddings
from app.models.all_models import ResponseModel

class SharedController(UtilityManager):
    def __init__(self) -> None:
        super().__init__()
        self.vectorstore = PGVectorEmbeddings()

    async def create_embeddings(self, files: List[UploadFile], collection_name:str = None) -> ResponseModel:
        uploaded = await self.upload(files=files)
        uploaded_dir = uploaded.get('directory')
        docs = self.load_directory(directory=uploaded_dir, chunk_size=1000, chunk_overlap=100)
        result = self.vectorstore.create_vector_embeddings(collection_name='vectorstore', docs=docs)
        return ResponseModel(message="Uploaded",data=[result],status_code=ResponseModel.CREATED_201)
 
    async def search_in_embedding(self,input:str,top_k:int, collection_name:str='langchain') -> ResponseModel:
        result =  self.vectorstore.search_in_vector(query=input)
        print("SEARCH:::", result)
        return ResponseModel(message="Result found",data=[{"content": result}])
    

    # async def delete_collection_embeddings(self, collection_name:str='langchain') -> ResponseModel:
    #     response =  await self.local_embedder.delete_collection_data( collection_name=collection_name)
    #     return ResponseModel(message="Deleted Successfully!",data=[{"content": response}])