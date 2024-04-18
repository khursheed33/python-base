import openai
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain_community.chat_models import ChatOpenAI
from langchain.agents.agent import AgentExecutor
from langchain.prompts import PromptTemplate


from app.utils.utility_manager import UtilityManager
from app.enums.env_keys import EnvKeys

class SQLAgentManager(UtilityManager):
    def __init__(self):
        super().__init__()
        self.OPENAI_KEY = self.get_env_variable(EnvKeys.APP_OPENAI_KEY.value)
        self.OPENAI_MODEL = self.get_env_variable(EnvKeys.APP_OPENAI_MODEL.value)
        self.OPENAI_TEMPERATURE = self.get_env_variable(EnvKeys.APP_OPENAI_TEMPERATURE.value)
        self.OPENAI_VERBOSE = self.get_env_variable(EnvKeys.APP_OPENAI_VERBOSE.value)
        openai.api_key = self.OPENAI_KEY

        self.DB_USER = self.get_env_variable(EnvKeys.POSTGRES_DB_USER.value)
        self.DB_PASSWORD = self.get_env_variable(EnvKeys.POSTGRES_DB_PASSWORD.value)
        self.DB_HOST = self.get_env_variable(EnvKeys.POSTGRES_DB_HOST.value)
        self.DB_PORT = self.get_env_variable(EnvKeys.POSTGRES_DB_PORT.value)
        self.DB_NAME = self.get_env_variable(EnvKeys.POSTGRES_DB_NAME.value)
        
        self.DB_CONNECTION = SQLDatabase.from_uri(
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}",
        )
        
        self.LLM = ChatOpenAI(model_name=self.OPENAI_MODEL, temperature=self.OPENAI_TEMPERATURE)
        
        # self.SQL_DB_TOOLKIT = SQLDatabaseChain.from_llm(llm=self.LLM, db=self.DB_CONNECTION, verbose=self.OPENAI_VERBOSE)
        self.SQL_DB_TOOLKIT = SQLDatabaseToolkit(db=self.DB_CONNECTION, llm=self.LLM)
        
    def run_sql_agent(self, prompt_template: PromptTemplate, agent_type:AgentType=AgentType.ZERO_SHOT_REACT_DESCRIPTION, return_intermediate_steps:bool=True):

        sql_agent:AgentExecutor = create_sql_agent(
            llm=self.LLM,
            toolkit=self.SQL_DB_TOOLKIT,
            verbose=self.OPENAI_VERBOSE,
            agent_type=agent_type,
            agent_executor_kwargs={"return_intermediate_steps": return_intermediate_steps}
        )
        
        result = sql_agent(prompt_template)
        
        return result
        
        



        