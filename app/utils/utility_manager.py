from app.utils.file_system import FileSystem
from app.utils.generate_uuid import generate_uuid
from app.utils.extract_data import extract_data
from app.utils.data_mapper import data_mapper
from app.utils.env_manager import EnvManager
from get_cwt import get_project_directory
class UtilityManager(FileSystem,EnvManager):
    def __init__(self):
        super().__init__()
    
    def generate_uuid(self):
        return generate_uuid()

    def extract_data(self, path:str):
        return extract_data(path=path)
    
    def data_mapper(self, prompt_template:str, kwargs:dict ):
        return data_mapper(prompt_template=prompt_template, kwargs=kwargs)
    
    def get_project_dir(self):
        return get_project_directory()
    
