import json
import logging
from typing import List

from fastapi import HTTPException
from app.databases.postgres_database_manager import PostgreSQLManager
from app.enums.env_keys import EnvKeys
from app.utils.utility_manager import UtilityManager
from langchain_core.documents import Document
from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings.azure_openai import AzureOpenAIEmbeddings

class PGVectorEmbeddings(UtilityManager):
    def __init__(self):
        super().__init__()
        self.__KEY = self.get_env_variable(EnvKeys.AZURE_EMBEDDING_KEY.value)
        self.__VERSION = self.get_env_variable(EnvKeys.AZURE_EMBEDDING_VERSION.value)
        self.__DEPLOYMENT = self.get_env_variable(EnvKeys.AZURE_EMBEDDING_DEPLOYMENT.value)
        self.__MODEL = self.get_env_variable(EnvKeys.AZURE_EMBEDDING_MODEL.value)
        self.__URL = self.get_env_variable(EnvKeys.AZURE_EMBEDDING_BASE_URL.value)
        
        self.__PG_HOST = self.get_env_variable(EnvKeys.POSTGRES_DB_HOST.value)
        self.__PG_PORT = self.get_env_variable(EnvKeys.POSTGRES_DB_PORT.value)
        self.__PG_USERNAME = self.get_env_variable(EnvKeys.POSTGRES_DB_USER.value)
        self.__PG_PASSWORD = self.get_env_variable(EnvKeys.POSTGRES_DB_PASSWORD.value)
        self.__PG_DATABASE = self.get_env_variable(EnvKeys.POSTGRES_DB_NAME.value)
        
        self.__CONNECTION_STRING = f"postgresql://{self.__PG_USERNAME}:{self.__PG_PASSWORD}@{self.__PG_HOST}:{self.__PG_PORT}/{self.__PG_DATABASE}"
        
        self.__EMBEDDINGS = AzureOpenAIEmbeddings(
            openai_api_key=self.__KEY,
            azure_deployment=self.__DEPLOYMENT,
            azure_endpoint=self.__URL,
            api_version=self.__VERSION,
            model=self.__MODEL,
        )
        self.__POSTGRES_DB = PostgreSQLManager()
        
    def get_pgvector(self) -> PGVector:
        vectorstore = PGVector(
            embedding_function=self.__EMBEDDINGS,
            collection_name='vectorstore',
            connection_string=self.__CONNECTION_STRING,
        )
        return vectorstore
    
    def create_vector_embeddings(self, docs: List[Document], collection_name:str = 'vectorstore') -> dict:
            result = self.get_pgvector().from_documents(
                embedding=self.__EMBEDDINGS,
                documents=docs,
                collection_name=collection_name,
                connection_string=self.__CONNECTION_STRING,
            )
            if result:
                return {"message": f"Embedding created successfully for: {collection_name}"}
            else:
                return {"error": "something went wrong!"}
    
    def search_in_vector(self, query:str, top_k:int = 3) -> dict:
        try:
            # If collection found then search
            vector_collection = self.get_pgvector()
            docs = vector_collection.similarity_search(query=query, k=top_k)
            formatted_documents = []
            for doc in docs:
                content = doc.page_content.strip()
                source = doc.metadata.get('source', 'Unknown Source')
                page = doc.metadata.get('page', 'Unknown Page')

                formatted_doc = f"Content:\n{content}\nSource: {source}\nPage: {page}\n"
                formatted_documents.append(formatted_doc)
            return formatted_documents
        except Exception as e:
            logging.error(msg=f"Something went wrong! {str(e)}")
            print("Embedding: ", str(e))
            return []
    
    def delete_vector(self, collection_name:str) -> dict:
        self.__POSTGRES_DB.delete_embeddings()
        return {"message": "Collection and embeddings deleted!"}
    
        