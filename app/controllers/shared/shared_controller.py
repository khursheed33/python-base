
import shutil
from typing import List
from fastapi import UploadFile,Body
from app.utils.utility_manager import UtilityManager
from app.llm.local_embeddings import ChromaVectorStoreWithLocalEmbeddings
from app.models.all_models import ResponseModel

class SharedController(UtilityManager):
    def __init__(self) -> None:
        super().__init__()
        self.local_embedder = ChromaVectorStoreWithLocalEmbeddings()

    async def create_embeddings(self, files: List[UploadFile]) -> ResponseModel:
        uploaded =await self.upload(files=files)
        res_data = uploaded.data[0]
        uploaded_dir = res_data.get('directory')
        await self.local_embedder.create_embeddings(document_path=uploaded_dir)
        
        # Delete the folder after processing
        shutil.rmtree(uploaded_dir)
        return ResponseModel(message=uploaded.message,data=[res_data],status_code=uploaded.status_code )
 
    async def search_in_embedding(self,input:str,top_k:int, collection_name:str='langchain') -> ResponseModel:
        result =  await self.local_embedder.search_in_vector(input=input, collection_name=collection_name,top_k=top_k)
        return ResponseModel(message="Result found",data=[{"content": result}])
    

    async def delete_collection_embeddings(self, collection_name:str='langchain') -> ResponseModel:
        response =  await self.local_embedder.delete_collection_data( collection_name=collection_name)
        return ResponseModel(message="Deleted Successfully!",data=[{"content": response}])