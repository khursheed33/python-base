import json
import pyodbc
from app.enums.env_keys import EnvKeys
from app.utils.utility_manager import UtilityManager
class SQLServerManager(UtilityManager):
    def __init__(self):
        super().__init__()
        self.conn_params = {
            'server': self.get_env_variable(EnvKeys.SQL_SERVER_SERVER.value),
            'database': self.get_env_variable(EnvKeys.SQL_SERVER_DATABASE.value),
            'username': self.get_env_variable(EnvKeys.SQL_SERVER_USERNAME.value),
            'password': self.get_env_variable(EnvKeys.SQL_SERVER_PASSWORD.value),
            'driver': self.get_env_variable(EnvKeys.SQL_SERVER_DRIVER.value),
            'autocommit': self.get_env_variable(EnvKeys.SQL_SERVER_AUTO_COMMIT.value)
        }

    def _get_connection(self):
        try:
            conn_str = ';'.join([f'{key}={value}' for key, value in self.conn_params.items()])
            connection = pyodbc.connect(conn_str)
            return connection
        except Exception as e:
            print('--CONN:Err:', str(e))

    def _execute_query(self, query, params=None, fetch_one=False, return_headers=False):
        conn = self._get_connection()
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if fetch_one:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall() if cursor.description else None

        if return_headers and cursor.description:
            headers = [column[0] for column in cursor.description]
            result = (headers, result)

        cursor.close()
        conn.close()
        return result

    def execute_generic_query(self, query, params=None, return_headers=False):
        try:
            return self._execute_query(query=query, params=params, return_headers=return_headers)
        except Exception as e:
            return f"Something went wrong! {str(e)}"
