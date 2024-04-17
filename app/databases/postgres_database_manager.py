import json
import psycopg2
from app.utils.utility_manager import UtilityManager
from app.enums.env_keys import EnvKeys

class PostgreSQLManager(UtilityManager):

    def __init__(self):
        super().__init__()
        self.conn_params = {
            'host': self.get_env_variable(EnvKeys.POSTGRES_DB_HOST.value),
            'database': self.get_env_variable(EnvKeys.POSTGRES_DB_NAME.value),
            'user': self.get_env_variable(EnvKeys.POSTGRES_DB_USER.value),
            'password': self.get_env_variable(EnvKeys.POSTGRES_DB_PASSWORD.value),
            'port': self.get_env_variable(EnvKeys.POSTGRES_DB_PORT.value)
        }
        
    def _get_connection(self):
        return psycopg2.connect(**self.conn_params)

    def _execute_query(self, query, params=None, fetch_one=False):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch_one:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall() if cursor.description else None
            conn.commit()
            cursor.close()
            conn.close()
            return result
        except (psycopg2.Error, Exception) as e:
            print("Error executing query:", e)
            return None
