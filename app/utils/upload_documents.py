from typing import List
from fastapi import UploadFile, HTTPException
import shutil
import os
import time
from app.enums.env_keys import EnvKeys
from app.utils.get_current_timestamp import get_current_timestamp_str
from app.utils.env_manager import EnvManager
from app.utils.file_system import FileSystem
ALLOWED_EXTENSIONS = ['.pdf', '.txt', '.docx']  # Add or remove extensions as needed

class FileUploadManager:
    def __init__(self) -> None:
        pass

    def upload(self, files: List[UploadFile]):
        upload_directory = f'{EnvManager().get_env_variable(EnvKeys.UPLOAD_DIR.value)}/{get_current_timestamp_str()}'
        FileSystem().create_folder(folder_path=upload_directory)
        for file in files:
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension not in ALLOWED_EXTENSIONS:
                raise HTTPException(status_code=400, detail=f"File extension '{file_extension}' is not allowed.")

            file_path = os.path.join(upload_directory, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            print(f"Uploaded file: {file.filename}")

        return {"message": "Files uploaded successfully","status":201, "directory":upload_directory}