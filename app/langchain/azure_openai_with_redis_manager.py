from langchain_openai import AzureChatOpenAI
from langchain.memory import  ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.output_parsers import StructuredOutputParser
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.prompts import ChatPromptTemplate
from app.enums.env_keys import EnvKeys
from app.utils.utility_manager import UtilityManager


class LLMWithRedisHistory(UtilityManager):
    def __init__(self):
            
        self.__AZURE_OPENAI_KEY = self.get_env_variable(EnvKeys.AZURE_OPENAI_KEY.value)
        self.__AZURE_TEMPERATURE = self.get_env_variable(EnvKeys.AZURE_OPENAI_TEMPERATURE.value)
        self.__AZURE_MODEL = self.get_env_variable(EnvKeys.AZURE_OPENAI_MODEL.value)
        self.__AZURE_BASE_URL = self.get_env_variable(EnvKeys.AZURE_OPENAI_BASE_URL.value)
        self.__AZURE_DEPLOYMENT = self.get_env_variable(EnvKeys.AZURE_OPENAI_DEPLOYMENT.value)
        self.__AZURE_VERSION = self.get_env_variable(EnvKeys.AZURE_OPENAI_API_VERSION.value)
        self.__AZURE_VERBOSE = bool(self.get_env_variable(EnvKeys.AZURE_OPENAI_VERBOSE.value))

        self.__REDIS_HOST = self.get_env_variable(EnvKeys.REDIS_HOST.value)
        self.__REDIS_PORT = self.get_env_variable(EnvKeys.REDIS_PORT.value)
        self.__REDIS_PASSWROD = self.get_env_variable(EnvKeys.REDIS_PASSWORD.value)
        self.__REDIS_DATABASE = self.get_env_variable(EnvKeys.REDIS_DATABASE.value)
        self.__CLEAR_INTERVAL = int(self.get_env_variable(EnvKeys.CLEAR_HISTORY_INTERVAL.value))
        
        self.llm_model = AzureChatOpenAI(
            model_name=self.__AZURE_MODEL,
            temperature=self.__AZURE_TEMPERATURE,
            api_key=self.__AZURE_OPENAI_KEY,
            api_version=self.__AZURE_VERSION,
            azure_deployment=self.__AZURE_DEPLOYMENT,
            azure_endpoint=self.__AZURE_BASE_URL,
            verbose=self.__AZURE_VERBOSE,
        )
        

    def run_chain(self,user_id:str, prompt: ChatPromptTemplate,output_parser: StructuredOutputParser = None, kwargs:dict = {}) -> dict:
        redis_history = RedisChatMessageHistory(
                    session_id=user_id, 
                    url=f"redis://:{self.__REDIS_PASSWROD}@{self.__REDIS_HOST}:{self.__REDIS_PORT}/{self.__REDIS_DATABASE}",
                    ttl=self.__CLEAR_INTERVAL,
                    )
        
        memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            chat_memory=redis_history,
        )
        
        chain = LLMChain(
            llm=self.llm_model,
            prompt=prompt,
            verbose=True,
            memory=memory
        )
        
        response = chain.invoke(input=kwargs)
        print("LLM-RES: ", response)
        
        if output_parser:
            result = output_parser.parse(response['text'])
            return result
        return response['text']