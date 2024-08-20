import os
from typing import Dict, List
from langchain.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.documents import Document
from app.enums.env_keys import EnvKeys
from app.utils.utility_manager import UtilityManager
from langchain_community.retrievers import (
    AzureCognitiveSearchRetriever
)

class AzureAISearchManager(UtilityManager):
    def __init__(self):
        self.azure_search_service_name = self.get_env_variable(EnvKeys.AZURE_SEARCH_SERVIC_NAME.value)
        self.azure_search_index_name = self.get_env_variable(EnvKeys.AZURE_AI_SEARCH_INDEX_NAME.value)
        self.azure_search_api_key = self.get_env_variable(EnvKeys.AZURE_SEARCH_API_KEY.value)
        self.azure_search_endpoint = self.get_env_variable(EnvKeys.AZURE_SEARCH_ENPOINT.value)
        
        self.azure_endpoint = self.get_env_variable(EnvKeys.AZURE_EMBEDDING_BASE_URL.value)
        self.azure_openai_api_key = self.get_env_variable(EnvKeys.AZURE_EMBEDDING_KEY.value)
        # self.azure_openai_api_version = self.get_env_variable(EnvKeys.AZURE_OPENAI_API_VERSION.value)
        self.azure_deployment = self.get_env_variable(EnvKeys.AZURE_EMBEDDING_DEPLOYMENT.value)

        self.embeddings = AzureOpenAIEmbeddings(
            model=self.azure_deployment,
            azure_endpoint=self.azure_endpoint,
            openai_api_key=self.azure_openai_api_key,
        )

        self.vector_store = AzureSearch(
            embedding_function=self.embeddings.embed_query,
            azure_search_endpoint=self.azure_search_endpoint,
            azure_search_key=self.azure_search_api_key,
            index_name=self.azure_search_index_name,
        )

    def create_embeddings(self, docs: List[Document]) -> dict:
        result = self.vector_store.add_documents(documents=docs)
        return result

    def search_in_vector(self, query: str, top_k: int = 3, filters: Dict = {}) -> List[Document]:
        retriever = AzureCognitiveSearchRetriever(
            top_k=top_k,
            index_name=self.azure_search_index_name,
            api_key=self.azure_search_api_key,
            service_name=self.azure_search_service_name,
            
        )
        search_results = retriever.invoke(input=query)
        return search_results
