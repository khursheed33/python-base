
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from app.utils.utility_manager import UtilityManager

class ChromaVectorStoreWithLocalEmbeddings(UtilityManager):
    def __init__(self):
        super().__init__()
        self.project_dir = self.get_project_dir()
        self.vector_path = 'app/vectors'
        self.create_folder(folder_path=self.vector_path)
        # Using OpenAI embeddings
        self.embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        self.vectordb = Chroma(persist_directory=self.vector_path, 
                               embedding_function=self.embedding)
        
    def create_embeddings(self, document_path: str, collection_name:str='langchain',chunk_size: int = 2000, chunk_overlap: int = 200):
        """Create a vector store from all .txt files in a directory."""
        try:
            all_documents = self.load_directory(directory=document_path, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            chroma_db = self.vectordb.from_documents(documents=all_documents, 
                                                     embedding=self.embedding,
                                                     collection_name=collection_name,
                                                     persist_directory=self.vector_path,
                                                     )
            chroma_db.persist()
            print('---Vector-Store-Created---')
        
        except Exception as e:
            print(f"Error creating vector store: {e}")
    
    def search_in_vector(self, input: str, top_k: int = 3,collection_name:str='langchain'):
        """Search for similar documents in the vector store based on a user question."""
        try:
            vectordb = Chroma(persist_directory=self.vector_path, 
                               embedding_function=self.embedding,
                               collection_name=collection_name,)
            response = vectordb.similarity_search(query=input, k=top_k)
            system_answer = '\n'.join(doc.page_content for doc in response)
            return system_answer
        
        except Exception as e:
            print(f"Error searching in vector store: {e}")
            return None
