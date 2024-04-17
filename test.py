from app.databases.sqlite_database_manager import SQLiteDBManager

db_managaer = SQLiteDBManager()
query = """
SELECT * FROM users;
"""
result = db_managaer._execute_query(query=query)

print(result)