import os

class EnvManager:
    def set_env_variable(key, value):
        os.environ[key] = value

    def get_env_variable(key):
        return os.environ[key]
