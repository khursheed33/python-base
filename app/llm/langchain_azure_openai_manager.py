from langchain_community.embeddings import AzureOpenAIEmbeddings
from langchain_community.chat_models.azure_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser
from app.utils.utility_manager import UtilityManager
from app.enums.env_keys import EnvKeys

class LangchainAzureOpenAIManager(UtilityManager):
    
    def __init__(self):
        super().__init__()
        self.API_KEY = self.get_env_variable(EnvKeys.AZURE_OPENAI_KEY.value)
        self.MODEL = self.get_env_variable(EnvKeys.AZURE_OPENAI_MODEL.value)
        self.DEPLOYMENT = self.get_env_variable(EnvKeys.AZURE_OPENAI_DEPLOYMENT.value)
        self.BASE_URL = self.get_env_variable(EnvKeys.AZURE_OPENAI_BASE_URL.value)
        self.VERSION = self.get_env_variable(EnvKeys.AZURE_OPENAI_API_VERSION.value)
        self.TEMPERATURE = self.get_env_variable(EnvKeys.AZURE_OPENAI_TEMPERATURE.value)
        
        self.EMBEDDINGS =  AzureOpenAIEmbeddings(model=self.MODEL, azure_deployment=self.DEPLOYMENT, base_url=self.BASE_URL, api_key=self.API_KEY)
        self.LLM = AzureChatOpenAI(model=self.MODEL, temperature=0, azure_endpoint=self.BASE_URL, api_version=self.VERSION, api_key=self.API_KEY, azure_deployment=self.DEPLOYMENT)


    def run_llm(self, prompt_template:PromptTemplate, output_parser:StructuredOutputParser=None):
        chain = prompt_template | self.LLM
        result =  chain.invoke({})
        if output_parser:
            return output_parser.parse(result)
        return result