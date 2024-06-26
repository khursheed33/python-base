
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from app.utils.utility_manager import UtilityManager

class ChromaVectorStoreWithLocalEmbeddings(UtilityManager):
    error_logger = UtilityManager()
    def __init__(self):
        super().__init__()
        self.project_dir = self.get_project_dir()
        self.vector_path = 'app/vectors'
        self.create_folder(folder_path=self.vector_path)
        self.embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    
    @error_logger.catch_api_exceptions
    async def create_embeddings(self, document_path: str, collection_name: str = 'langchain', chunk_size: int = 2000, chunk_overlap: int = 200):
        """Create a vector store from all .txt files in a directory."""
        all_documents = self.load_directory(directory=document_path, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        vectordb = Chroma(persist_directory=self.vector_path, embedding_function=self.embedding,collection_name=collection_name)
        chroma_db = vectordb.from_documents(documents=all_documents, embedding=self.embedding, collection_name=collection_name, persist_directory=self.vector_path)
        chroma_db.persist()
        return "Vector store created"

    @error_logger.catch_api_exceptions
    async  def search_in_vector(self, input: str, top_k: int = 3, collection_name: str = 'langchain'):
        """Search for similar documents in the vector store based on a user question."""
        vectordb = Chroma(persist_directory=self.vector_path, embedding_function=self.embedding, collection_name=collection_name)
        search_response = vectordb.similarity_search(query=input, k=top_k)
        formatted_res = '\n'.join(doc.page_content for doc in search_response)
        return formatted_res
    
    @error_logger.catch_api_exceptions
    async def delete_collection_data(self, collection_name: str):
        """Delete the data for a specific collection from the vector store."""
        vectordb = Chroma(persist_directory=self.vector_path, embedding_function=self.embedding,collection_name=collection_name)
        vectordb.delete_collection()
        message = f"Collection '{collection_name}' has been deleted from the vector store."
        return message