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

    def find_collection(self, collection_id: str = 'vectorstore'):
        try:
            __findcollection_query = "SELECT * FROM langchain_pg_collection WHERE name = %s"
            found_collection, headers = self._execute_query(__findcollection_query, (collection_id,), return_headers=True)
            if found_collection:
                result_dict = [dict(zip(headers, row)) for row in found_collection]
                return result_dict
            else:
                return []
        except Exception as e:
            tb = traceback.format_exc()
            logging.info(f"Traceback : {tb}")
            logging.error(f"exception in find_collection : {e}")
            return {"error": str(e)}

    def delete_embeddings(self, collection_id: str = 'vectorstore'):
        try:
            collection = self.find_collection(collection_id=collection_id)
            collection_id = collection[0]['uuid']
            delete_collection_query = "DELETE FROM langchain_pg_collection WHERE uuid = %s"
            delete_embedding_query = "DELETE FROM langchain_pg_embedding WHERE collection_id = %s"
            self._execute_query(delete_collection_query, (collection_id,))
            self._execute_query(delete_embedding_query, (collection_id,))
            return {"status": "Deleted successfully!"}
        except Exception as e:
            tb = traceback.format_exc()
            logging.info(f"Traceback : {tb}")
            logging.error(f"exception in delete_embeddings : {e}")
            return {"error": str(e)}

    def search_in_embeddings(self, query: str, collection_uuid: str, top_k=4):
        try:
            sql_query = '''
                SELECT document FROM langchain_pg_embedding  
                WHERE collection_id = %s
                ORDER BY embedding <=> %s 
                LIMIT %s;
            '''
            params = (collection_uuid, query, top_k)
            results, headers = self._execute_query(sql_query, params, return_headers=True)
            if results:
                result_dict = [dict(zip(headers, row)) for row in results]
                return result_dict
            else:
                return []
        except Exception as e:
            tb = traceback.format_exc()
            logging.info(f"Traceback : {tb}")
            logging.error(f"exception in search_in_embeddings : {e}")
            return {"error": str(e)}
