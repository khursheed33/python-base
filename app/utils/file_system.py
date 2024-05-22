import os
import shutil
from pathlib import Path

class FileSystem:
    def __init__(self) -> None:
        pass

    def create_file(self, file_path: str):
        file_path = self.clean_path(path=file_path)
        if not os.path.exists(file_path):
            with open(file_path, "x"):
                print("File Created: ", file_path)

    def clean_path(self, path: str) -> str:
        cleaned_path = path.replace("\\", "/")
        cleaned_path = os.path.normpath(cleaned_path)
        return cleaned_path

    def create_folder(self, folder_path: str):
        folder_path = self.clean_path(path=folder_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
            print("Folder Created: ", folder_path)

    def delete_file(self, file_path: str) -> bool:
        file_path = self.clean_path(path=file_path)
        try:
            os.remove(file_path)
            print(f"File '{file_path}' deleted successfully.")
            return True
        except Exception as e:
            print(f"Error deleting file '{file_path}': {e}")
            return False

    def delete_folder(self, folder_path: str) -> bool:
        folder_path = self.clean_path(path=folder_path)
        try:
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' deleted successfully.")
            return True
        except Exception as e:
            print(f"Error deleting folder '{folder_path}': {e}")
            return False

    def create_and_get_upload_dir(self, folder_name: str) -> Path:
        base_upload_path = str(os.environ.get("UPLOAD_DIR"))
        upload_location = Path(base_upload_path) / folder_name
        upload_location.mkdir(parents=True, exist_ok=True)
        return upload_location

    def get_project_dir(self) -> Path:
        current_file = Path(__file__).resolve()
        project_dir = current_file.parent.parent.parent # app <- utils <-
        return project_dir