import os
from langchain_community.vectorstores.chroma import Chroma
from typing import List
from app.enums.env_keys import EnvKeys
from app.utils.utility_manager import UtilityManager
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.document_loaders.text import TextLoader
import glob
class ChromaVectorStoreManager(UtilityManager):
    def __init__(self, chunk_size: int = 2000):
        super().__init__()
        self.project_dir = self.get_project_dir()
        self.vector_path = self.clean_path(f'{self.project_dir}/app/vectors')
        os.makedirs(self.vector_path, exist_ok=True)
        # Using OpenAI embeddings
        self.embedding = OpenAIEmbeddings(openai_api_key=self.get_env_variable(EnvKeys.APP_OPENAI_KEY.value), chunk_size=chunk_size)
        self.vectordb = Chroma(persist_directory=self.vector_path, 
                               embedding_function=self.embedding)
        
    def create_vector_store(self, document_path: str, collection_name:str='langchain',chunk_size: int = 2000, chunk_overlap: int = 200):
        """Create a vector store from all .txt files in a directory."""
        try:
            txt_files = glob.glob(os.path.join(document_path, "*.txt"))
            all_documents = []
            for txt_file in txt_files:
                loader = TextLoader(file_path=self.clean_path(txt_file))
                documents = loader.load()
                all_documents.extend(documents)
            
            chroma_db = self.vectordb.from_documents(documents=all_documents, 
                                                     embedding=self.embedding,
                                                     collection_name=collection_name,
                                                     persist_directory=self.vector_path,
                                                     )
            chroma_db.persist()
            print('---Vector-Store-Created---')
        
        except Exception as e:
            print(f"Error creating vector store: {e}")
    
    def search_in_vector(self, user_question: str, top_k: int = 3,collection_name:str='langchain'):
        """Search for similar documents in the vector store based on a user question."""
        try:
            response = self.vectordb.similarity_search(query=user_question, k=top_k, collection_name=collection_name)
            system_answer = '\n'.join(doc.page_content for doc in response)
            return system_answer
        
        except Exception as e:
            print(f"Error searching in vector store: {e}")
            return None
