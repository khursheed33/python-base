import boto3
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain, LLMChain
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import PromptTemplate
from app.utils.utility_manager import UtilityManager
from app.enums.env_keys import EnvKeys



class LangchainBedrockManager(UtilityManager):
    def __init__(self):
        super().__init__()
        self.MODEL_ID = self.get_env_variable(EnvKeys.APP_CLAUDE_MODEL_ID.value)
        self.REGION = self.get_env_variable(EnvKeys.APP_AWS_REGION_NAME.value)
        self.SERVICE_NAME = self.get_env_variable(EnvKeys.APP_AWS_SERVICE_NAME.value)
        self.SECRET_ACCESS_KEY = self.get_env_variable(EnvKeys.APP_AWS_SECRET_ACCESS_KEY.value)
        self.ACCESS_KEY_ID = self.get_env_variable(EnvKeys.APP_AWS_ACCESS_KEY_ID.value)
        
        self.BOTO_BEDROCK_CLIENT = boto3.client(
        service_name=self.SERVICE_NAME,
        region_name=self.REGION, 
        aws_access_key_id=self.ACCESS_KEY_ID,
        aws_secret_access_key=self.SECRET_ACCESS_KEY
        )
        
        self.BEDROCK_LLM =  Bedrock(
        model_id=self.MODEL_ID,
        client=self.BOTO_BEDROCK_CLIENT,
        )
        
        self.conversation_memory = ConversationBufferMemory(
        llm=self.BEDROCK_LLM)

        self.conversation_chain = ConversationChain(
            llm=self.BEDROCK_LLM, memory=self.conversation_memory, verbose=False)

    def run_conversational_chain(self, prompt: str, output_parser: StructuredOutputParser = None) -> dict:
        """
        This LLM chain has memory, Chats will be stored by default.
        """
        response = self.conversation_chain.predict(input=prompt)

        if output_parser:
            parsed_response = output_parser.parse(response)
            return parsed_response

        return {"response": response}

    def run_llm_chain(self, prompt_template: PromptTemplate, output_parser: StructuredOutputParser = None, input_values: dict = {}) -> dict:
        """
        This LLM chain without memory, Chats will be stored by default.
        """
        llm_chain = LLMChain(
            llm=self.BEDROCK_LLM,
            prompt=prompt_template,
        )

        result = llm_chain.run(input_values)

        if output_parser:
            return output_parser.parse(result)

        return {"response": result}

