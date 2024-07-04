from enum import Enum

class EnvKeys(Enum):
    APP_HOST='APP_HOST'
    APP_PORT='APP_PORT'
    APP_ENVIRONMENT = "APP_ENVIRONMENT"
    # FOLDERS
    UPLOAD_DIR = 'UPLOAD_DIR'
    UPLOAD_ALLOWED_EXTENTIONS = 'UPLOAD_ALLOWED_EXTENTIONS'
    # URLs
    LOCAL_LLM_URL = 'LOCAL_LLM_URL'
    # LLM
    APP_OPENAI_KEY = 'APP_OPENAI_KEY'
    APP_OPENAI_MODEL = 'APP_OPENAI_MODEL'
    APP_OPENAI_VERBOSE='APP_OPENAI_VERBOSE'
    APP_OPENAI_TEMPERATURE = 'APP_OPENAI_TEMPERATURE'
    # Azure OpenAI
    AZURE_OPENAI_KEY='AZURE_OPENAI_KEY'
    AZURE_OPENAI_MODEL='AZURE_OPENAI_MODEL'
    AZURE_OPENAI_TEMPERATURE='AZURE_OPENAI_TEMPERATURE'
    AZURE_OPENAI_DEPLOYMENT='AZURE_OPENAI_DEPLOYMENT'
    AZURE_OPENAI_BASE_URL='AZURE_OPENAI_BASE_URL'
    AZURE_OPENAI_API_VERSION='AZURE_OPENAI_API_VERSION'
    # Claude
    APP_CLAUDE_MODEL_ID = 'APP_CLAUDE_MODEL_ID'
    APP_CLAUDE_TEMPARATURE = 'APP_CLAUDE_TEMPARATURE'
    APP_AWS_SECRET_ACCESS_KEY = 'APP_AWS_SECRET_ACCESS_KEY'
    APP_AWS_ACCESS_KEY_ID = 'APP_AWS_ACCESS_KEY_ID'
    APP_AWS_REGION_NAME = 'APP_AWS_REGION_NAME'
    APP_AWS_SERVICE_NAME = 'APP_AWS_SERVICE_NAME'
    # Logging settings
    LOG_LEVEL='LOG_LEVEL'
    LOG_FILE='LOG_FILE'
    APP_LOGGING_LEVEL='APP_LOGGING_LEVEL'
    APP_LOGGING_HANDLER_NAME='APP_LOGGING_HANDLER_NAME'
    APP_LOGGING_FOLDER='APP_LOGGING_FOLDER'
    APP_LOGGING_FORMATTER='APP_LOGGING_FORMATTER'
    APP_LOGGING_DATEFORMAT='APP_LOGGING_DATEFORMAT'
    APP_LOGGING_MAXBYTES='APP_LOGGING_MAXBYTES'
    APP_LOGGING_BACKUPCOUNT='APP_LOGGING_BACKUPCOUNT'
    # SQLITE
    SQLITE_DB_PATH= 'SQLITE_DB_PATH'
    #POSTGRES
    POSTGRES_DB_HOST='POSTGRES_DB_HOST'
    POSTGRES_DB_NAME='POSTGRES_DB_NAME'
    POSTGRES_DB_USER='POSTGRES_DB_USER'
    POSTGRES_DB_PASSWORD='POSTGRES_DB_PASSWORD'
    POSTGRES_DB_PORT='POSTGRES_DB_PORT'
    POSTGRES_DB_SCHEMA='POSTGRES_DB_NAME'
    # MSSQL
    SQL_SERVER_SERVER='SQL_SERVER_SERVER'
    SQL_SERVER_DATABASE='SQL_SERVER_DATABASE'
    SQL_SERVER_USERNAME='SQL_SERVER_USERNAME'
    SQL_SERVER_PASSWORD='SQL_SERVER_PASSWORD'
    SQL_SERVER_DRIVER='SQL_SERVER_DRIVER'
    SQL_SERVER_AUTO_COMMIT='SQL_SERVER_AUTO_COMMIT'
    # MONGODB
    MONGODB_CONNECTION_STRING='MONGODB_CONNECTION_STRING'
    MONGODB_DB_NAME='MONGODB_DB_NAME'
    MONGODB_DB_USERNAME='MONGODB_DB_USERNAME'
    MONGODB_DB_PASSWORD='MONGODB_DB_PASSWORD'
    MONGODB_DB_HOST='MONGODB_DB_HOST'
    MONGODB_DB_PORT='MONGODB_DB_PORT'
    
    # Authentication
    KEYCLOACK_BASE_URL='KEYCLOACK_BASE_URL'
    KEYCLOACK_REALM_NAME='KEYCLOACK_REALM_NAME'
    KEYCLOACK_CLIENT_ID='KEYCLOACK_CLIENT_ID'
    
    SECRET_KEY='SECRET_KEY'
    ALGORITHM='ALGORITHM'
    ACCESS_TOKEN_EXPIRE_MINUTES='ACCESS_TOKEN_EXPIRE_MINUTES'
    
    AZURE_AD_TENANT_ID = "AZURE_AD_TENANT_ID"
    AZURE_AD_CLIENT_ID = "AZURE_AD_CLIENT_ID"
    AZURE_AD_CLIENT_SECRET = "AZURE_AD_CLIENT_SECRET"
