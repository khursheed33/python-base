import json
import redis

from app.enums.env_keys import EnvKeys
from app.utils.utility_manager import UtilityManager

class RedisManager(UtilityManager):
    def __init__(self):
        self.__HOST = self.get_env_variable(EnvKeys.REDIS_HOST.value)
        self.__PORT = self.get_env_variable(EnvKeys.REDIS_PORT.value)
        self.__PASSWROD = self.get_env_variable(EnvKeys.REDIS_PASSWORD.value)
        self.__DATABASE = self.get_env_variable(EnvKeys.REDIS_DATABASE.value)
        
        self.redis_client = redis.StrictRedis(
            host=self.__HOST,
            port=self.__PORT,
            password=self.__PASSWROD,
            db=self.__DATABASE,
            decode_responses=True  # To get string responses instead of bytes
        )

    def set_value(self, key, value):
        """
        Set the value for a given key.
        """
        try:
            self.redis_client.set(key, json.dumps(value))
            print(f"Value set for key: {key}")
        except Exception as e:
            print(f"Error setting value: {e}")

    def get_value(self, key):
        """
        Get the value for a given key.
        """
        try:
            value = self.redis_client.get(key)
            if value is None:
                print(f"No value found for key: {key}")
            return json.loads(value)
        except Exception as e:
            print(f"Error getting value: {e}")

    def delete_value(self, key):
        """
        Delete the value for a given key.
        """
        try:
            result = self.redis_client.delete(key)
            if result == 1:
                print(f"Key deleted: {key}")
            else:
                print(f"Key not found: {key}")
        except Exception as e:
            print(f"Error deleting key: {e}")

    def update_value(self, key, value):
        """
        Update the value for a given key. This is effectively the same as set_value.
        """
        self.set_value(key, value)
