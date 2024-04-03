from dotenv import load_dotenv
import os
import logging
from app.utils.file_system import FileSystem
import sys

class Settings:
    def __init__(self):
        load_dotenv()
        
        self.APP_ENV = os.getenv("APP_ENV", "DEVELOPMENT")
        self.APP_HOST = os.getenv("APP_HOST", "localhost")
        self.APP_PORT = int(os.getenv("APP_PORT", 3301))
        
        # Ensure logs directory exists
        logs_dir = 'logs'
        FileSystem.create_folder(logs_dir)
        
        # Create log file path
        log_file_path = os.path.join(logs_dir, 'log.log')
        
        # Logging configuration
        log_level = os.getenv("APP_LOG_LEVEL", "INFO")
        log_file = os.getenv("APP_LOG_FILE", log_file_path)
        print("Logs: ", log_file)
            
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s",
            filename=log_file,
        )
        
        if self.APP_ENV == "PRODUCTION":
            sys.stdout = open(os.devnull, 'w')
            sys.stderr = open(os.devnull, 'w')