import glob
import os
from typing import List, Optional, Union
from langchain.document_loaders.text import TextLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.utils.utility_manager import UtilityManager

class DocumentLoader:
    @staticmethod
    def load_directory(directory: str, chunk_size: int = 2000, chunk_overlap: int = 150) -> List[Document]:
        all_documents = []
        for file_path in glob.glob(os.path.join(directory, "*")):
            loader = DocumentLoader.get_loader(file_path)
            if loader:
                documents = loader.load()
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                texts = text_splitter.split_documents(documents)
                all_documents.extend(texts)
        return all_documents

    @staticmethod
    def load_file(file_path: str, chunk_size: int = 2000, chunk_overlap: int = 150) -> List[Document]:
        loader = DocumentLoader.get_loader(file_path)
        if loader:
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            texts = text_splitter.split_documents(documents)
            return texts
        else:
            return []

    @staticmethod
    def get_loader(file_path: str) -> Optional[Union[TextLoader, WebBaseLoader]]:
        cleaned_path = UtilityManager.clean_path(file_path)

        if cleaned_path.startswith("http"):
            return WebBaseLoader(cleaned_path)
        else:
            file_extension = os.path.splitext(cleaned_path)[1].lower()
            if file_extension == ".pdf":
                return PyPDFLoader(cleaned_path)
            elif file_extension == ".docx":
                return Docx2txtLoader(cleaned_path)
            elif file_extension == ".txt":
                return TextLoader(cleaned_path)
            elif file_extension == ".csv":
                return CSVLoader(cleaned_path)
            else:
                return None