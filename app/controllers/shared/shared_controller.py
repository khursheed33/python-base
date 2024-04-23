
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

    
    def create_embeddings(self, files: List[UploadFile]):
        uploaded = self.upload(files=files)
        uploaded_dir = uploaded.get('directory')
        self.local_embedder.create_embeddings(document_path=uploaded_dir)
        # Delete the folder after processing
        shutil.rmtree(uploaded_dir)
        return ResponseModel(message=uploaded.get('message'),status_code=uploaded.get('status') )
        
        
    def search_in_embedding(self,input:str,top_k:int, collection_name:str='langchain'):
        return self.local_embedder.search_in_vector(input=input, collection_name=collection_name,top_k=top_k)
    
    def delete_collection_embeddings(self, collection_name:str='langchain'):
        return self.local_embedder.delete_collection_data( collection_name=collection_name)
