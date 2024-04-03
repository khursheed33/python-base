import os

class FileSystem:
    def create_file(file_path:str):
        if not os.path.exists(FileSystem.clean_path(file_path)):
            with open(file_path, "x"):
                print("File Created: ", file_path)
                pass
            
    def clean_path(directory:str):
        """
        Clean a file path to ensure compatibility across different operating systems.
        """
        cleaned_path = directory.replace("\\", "/")
        cleaned_path = os.path.normpath(cleaned_path)
        return cleaned_path

    def create_folder(folder_path:str):
        if not os.path.exists(folder_path):
            os.makedirs(FileSystem.clean_path(folder_path))
            print("Folder Created: ",folder_path)