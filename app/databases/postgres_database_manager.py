import json
import psycopg2
import traceback
import logging
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

    def _execute_query(self, query, params=None, fetch_one=False, return_headers=False):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch_one:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall() if cursor.description else None
            headers = [desc[0] for desc in cursor.description] if cursor.description else []
            conn.commit()
            cursor.close()
            conn.close()
            if return_headers:
                return result, headers
            return result
        except (psycopg2.Error, Exception) as e:
            logging.error("Error executing query:", e)
            return None

    def delete_embeddings(self, collection_id:str = 'vectorstore'):
        try:
            delete_collection_query = "DELETE FROM langchain_pg_collection WHERE uuid = %s"
            delete_embedding_query = "DELETE FROM langchain_pg_embedding WHERE collection_id = %s"
            self._execute_query(delete_collection_query, (collection_id,))
            self._execute_query(delete_embedding_query, (collection_id,))
            return "Deleted successfully!"
        except Exception as e:
            tb = traceback.format_exc()
            logging.info(f"Traceback : {tb}")
            logging.error(f"exception in delete_embeddings : {e}")

    def search_in_embeddings(self, query:str, collection_name:str, top_k=5):
        try:
            sql_query = f'''
                SELECT document FROM langchain_pg_embedding  
                WHERE collection_id = %s
                ORDER BY embedding <=> %s 
                LIMIT %s;
            '''
            params = (collection_name, query, top_k)
            results = self._execute_query(sql_query, params)
            return results       
        except Exception as e:
            tb = traceback.format_exc()
            logging.info(f"Traceback : {tb}")
            logging.error(f"exception in search_in_embeddings : {e}")

