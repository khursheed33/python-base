import os
import logging
from app.utils.file_system import FileSystem
import sys
import logging.handlers 
from dotenv import load_dotenv
import socket
from app.utils.utility_manager import UtilityManager
from app.enums.env_keys import EnvKeys
from app.enums.app_env_type import AppEnvironment
class Settings(UtilityManager):
    
    def __init__(self):
        super().__init__()
        try:
            load_dotenv(".env.example")
            self.APP_HOST = self.get_env_variable(EnvKeys.APP_HOST.value)
            self.APP_PORT = int(self.get_env_variable(EnvKeys.APP_PORT.value))
            self.APP_ENVIRONMENT =  self.get_env_variable(EnvKeys.APP_ENVIRONMENT.value)
            fmt =  self.get_env_variable(EnvKeys.APP_LOGGING_FORMATTER.value)
            level =  self.get_env_variable(EnvKeys.APP_LOGGING_LEVEL.value)
            logging.getLogger().handlers.clear()
            # Ensure logs directory exists
            logs_dir = 'logs'
            FileSystem.create_folder(logs_dir)
            
            logging.basicConfig(
                handlers=[logging.handlers.RotatingFileHandler(
                     self.get_env_variable(EnvKeys.APP_LOGGING_FILE.value),
                    maxBytes=int( self.get_env_variable(EnvKeys.APP_LOGGING_MAXBYTES.value)),
                    backupCount=int( self.get_env_variable(EnvKeys.APP_LOGGING_BACKUPCOUNT.value)))  
                ],
                level=level,
                format=fmt,
                datefmt= self.get_env_variable(EnvKeys.APP_LOGGING_DATEFORMAT.value)
            )
            # set up logging to console
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            # set a format which is simpler for console use
            formatter = logging.Formatter(fmt)
            console.setFormatter(formatter)
            # add the handler to the root logger
            logging.getLogger('').addHandler(console)
            logging.info(f"Logging Configuration Set:{level}")

            logging.getLogger('watchfiles').setLevel(logging.ERROR)
            # Disable Prints in Production
            if self.APP_ENVIRONMENT == AppEnvironment.DEV.value:
                sys.stdout = open(os.devnull, 'w')
                sys.stderr = open(os.devnull, 'w')
        except Exception as err:
            logging.error(f"Error setting up logging configuration:{err}")
            raise err

    def get_hostname(self) -> str:
        hostname = socket.gethostname()
        return hostname