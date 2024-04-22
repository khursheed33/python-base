import json
from pymongo import MongoClient
from app.utils.utility_manager import UtilityManager
from app.enums.env_keys import EnvKeys

class MongoDBManager(UtilityManager):

    def __init__(self):
        super().__init__()
        self.client = MongoClient(self.get_env_variable(EnvKeys.MONGODB_CONNECTION_STRING.value))
        self.db = self.client[self.get_env_variable(EnvKeys.MONGODB_DB_NAME.value)]

    def _execute_query(self, collection_name, query, params=None, fetch_one=False, aggregate=False):
        try:
            collection = self.db[collection_name]
            if aggregate:
                result = collection.aggregate(query)
                if fetch_one:
                    result = next(result, None)
                else:
                    result = list(result)
            else:
                if fetch_one:
                    result = collection.find_one(query, params)
                else:
                    result = list(collection.find(query, params))
            return result
        except Exception as e:
            print("Error executing query:", e)
            return None
