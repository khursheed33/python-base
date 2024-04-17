import os

class EnvManager:
    def __init__(self):
        pass
    def set_env_variable(self,key, value):
        os.environ[key] = value

    def get_env_variable(self, key):
        return os.environ[key]
