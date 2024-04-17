import os

class EnvManager:
    def set_env_variable(self,key, value):
        os.environ[key] = value

    def get_env_variable(self,key):
        return os.environ[key]
