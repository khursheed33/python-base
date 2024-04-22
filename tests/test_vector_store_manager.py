import os
import pytest
from app.llm.vector_store_manager import ChromaVectorStoreManager

@pytest.fixture
def vector_manager():
    return ChromaVectorStoreManager()

def test_create_vector_store(vector_manager):
    document_path = "mock/docs"
    collection_name = "langchain"
    vector_manager.create_vector_store(document_path, collection_name)
    assert os.path.exists(vector_manager.vector_path)
    assert os.path.exists(os.path.join(vector_manager.vector_path, f"{collection_name}.hdf5"))

def test_search_in_vector(vector_manager):
    user_question = "What is the capital of France?"
    top_k = 3
    collection_name = "langchain"
    response = vector_manager.search_in_vector(user_question, top_k, collection_name)
    assert response is not None
    assert isinstance(response, str)

