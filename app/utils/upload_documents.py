from typing import List
from fastapi import UploadFile,File, HTTPException
import shutil
import os
from app.enums.env_keys import EnvKeys
from app.utils.get_current_timestamp import get_current_timestamp_str
from app.utils.env_manager import EnvManager
from app.utils.file_system import FileSystem
from app.models.all_models import ResponseModel
import ast
class FileUploadManager:
    def __init__(self) -> None:
        pass
    
    async def upload(self, files: List[UploadFile]) -> ResponseModel:
        env_manager = EnvManager()
        ALLOWED_EXTENSIONS = ast.literal_eval(env_manager.get_env_variable(EnvKeys.UPLOAD_ALLOWED_EXTENTIONS.value))
        upload_directory = f'{env_manager.get_env_variable(EnvKeys.UPLOAD_DIR.value)}/{get_current_timestamp_str()}'
        FileSystem().create_folder(folder_path=upload_directory)

        for file in files:
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension not in ALLOWED_EXTENSIONS:
                raise HTTPException(status_code=ResponseModel.NOT_ALLOWED_400, detail=f"File extension '{file_extension}' is not allowed.")

            file_path = os.path.join(upload_directory, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            print(f"Uploaded file: {file.filename}")
        return ResponseModel(message="Files uploaded successfully",status_code=ResponseModel.CREATED, data=[{"message": "Files uploaded successfully","status":ResponseModel.CREATED, "directory":upload_directory}])