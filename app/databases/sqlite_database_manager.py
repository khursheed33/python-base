import json
import sqlite3
from sqlite3 import Error
from datetime import datetime
from app.utils.utility_manager import UtilityManager
from app.enums.env_keys import EnvKeys


class SQLiteDBManager(UtilityManager):
    _instance = None
    
    def __init__(self):
        super().__init__()

    def __new__(self):
        if self._instance is None:
            self._instance = super(SQLiteDBManager, self).__new__(self)
            project_dir = self.get_project_dir()
            db_path = f"{project_dir}/{self.get_env_variable(EnvKeys.SQLITE_DB_PATH.value)}"
            db_path = self.clean_path(db_path)
            self._instance.conn_params = {
                'database':db_path,
            }
            
        return self._instance

    def _get_connection(self):
        try:
            conn = sqlite3.connect(**self.conn_params)
            return conn
        except Error as e:
            print(f"Error connecting to SQLite database: {e}")
            return None

    def _execute_query(self, query, params=None, fetch_one=False):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch_one:
                result = cursor.fetchone()
                if result:
                    column_names = [column[0] for column in cursor.description]
                    result = dict(zip(column_names, result))
            else:
                result = cursor.fetchall() if cursor.description else None
                if result:
                    column_names = [column[0] for column in cursor.description]
                    # Convert each row to a dictionary
                    result = [dict(zip(column_names, row)) for row in result]

            conn.commit()
            if result:
                # Convert to JSON string here
                result = json.loads(json.dumps(result))
            print("---Query-Executed--Successfully----")
            return result
        
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

