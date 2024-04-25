# from app.databases.sqlite_database_manager import SQLiteDBManager

# db_managaer = SQLiteDBManager()
# query = """
# SELECT * FROM users;
# """
# result = db_managaer._execute_query(query=query)

# print(result)


# from app.databases.postgres_database_manager import PostgreSQLManager

# db_managaer = PostgreSQLManager()
# print("isntance:", db_managaer)
# query = """
# SELECT * FROM users;
# """
# result = db_managaer._execute_query(query=query)

# print(result)

from app.constants.log_messages import LogMessages

print(LogMessages.CREATE_VECTOR_ERROR.format("Hello"))