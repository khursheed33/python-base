import hashlib
import logging
from typing import Dict, List
from app.enums.env_keys import EnvKeys
from app.utils.file_system import FileSystem
from app.utils.generate_uuid import generate_uuid
from app.utils.extract_data import extract_data
from app.utils.data_mapper import data_mapper
from app.utils.get_current_timestamp import calculate_response_time, get_current_timestamp_str
from app.utils.env_manager import EnvManager
from app.utils.document_loader import DocumentLoader
from app.utils.api_error_handler import CatchAPIException

class UtilityManager(FileSystem, EnvManager, DocumentLoader,CatchAPIException):
    def __init__(self):
        super().__init__()
    
    def generate_uuid(self):
        return generate_uuid()

    def extract_data(self, path:str):
        return extract_data(path=path)
    
    def data_mapper(self, prompt_template:str, kwargs:dict ):
        return data_mapper(prompt_template=prompt_template, kwargs=kwargs)
    
    def get_current_timestamp_str(self):
        return get_current_timestamp_str()
    
    def str_to_bool(self, value:str):
        if value.lower() in ('true', '1', 'yes'):
            return True
        elif value.lower() in ('false', '0', 'no'):
            return False
        else:
            return False
        
    def prepare_source_url(self, sources:List[str]) -> Dict:
        base_url= self.get_env_variable(EnvKeys.SOURCE_BASE_URL.value)
        source_urls = {}
        if sources and len(sources) > 0:
            source_urls = {source: base_url + source for source in sources}
        return source_urls
     
    def create_new_checksum(self, file_path: str) -> str:
        try:
            # Calculate SHA-256 checksum of the file
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            checksum = sha256_hash.hexdigest()
            return checksum
        except Exception as e:
            logging.error("Error creating checksum")
            raise e
    def calculate_response_time(self,start_time):
        return calculate_response_time(start_time)
        
