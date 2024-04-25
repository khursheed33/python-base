import os
import shutil

class FileSystem:
    def __init__(self) -> None:
        pass
    def create_file(self,file_path:str):
        if not os.path.exists(self.clean_path(path=file_path)):
            with open(file_path, "x"):
                print("File Created: ", file_path)
                pass
            
    def clean_path(self,path:str) -> str:
        """
        Clean a file path to ensure compatibility across different operating systems.
        """
        cleaned_path = path.replace("\\", "/")
        cleaned_path = os.path.normpath(cleaned_path)
        return cleaned_path

    def create_folder(self,folder_path:str):
        if not os.path.exists(folder_path):
            os.makedirs(self.clean_path(path=folder_path),exist_ok=True)
            print("Folder Created: ",folder_path)
            

    def delete_file(self,file_path:str)->bool:
        """
        Delete a file.

        Args:
            file_path (str): The path to the file to be deleted.

        Returns:
            bool: True if the file was successfully deleted, False otherwise.
        """
        try:
            file_path = self.clean_path(path=file_path)
            os.remove(file_path)
            print(f"File '{file_path}' deleted successfully.")
            return True
        except Exception as e:
            print(f"Error deleting file '{file_path}': {e}")
            return False

    def delete_folder(self,folder_path:str) -> bool:
        """
        Delete a folder and its contents recursively.

        Args:
            folder_path (str): The path to the folder to be deleted.

        Returns:
            bool: True if the folder was successfully deleted, False otherwise.
        """
        try:
            folder_path = self.clean_path(path=folder_path)
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' deleted successfully.")
            return True
        except Exception as e:
            print(f"Error deleting folder '{folder_path}': {e}")
            return False
