import os
from langchain_community.chat_models import ChatOpenAI
from get_cwt import get_project_directory
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain, LLMChain
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import PromptTemplate
from app.utils.utility_manager import UtilityManager
from app.enums.env_keys import EnvKeys

class LangchainOpenAIManager(UtilityManager):
    def __init__(self):
        super().__init__()
        self.key = self.get_env_variable(EnvKeys.APP_OPENAI_KEY.value)
        
        # TODO 
        # self.llm_model = ChatOpenAI(
        #     model_name=self.config["open_ai"]["model"], temperature=self.config["open_ai"]["temperature"])

        # self.conversation_memory = ConversationBufferMemory(
        #     llm=self.llm_model)
        
        # self.conversation_chain = ConversationChain(
        #     llm=self.llm_model, memory=self.conversation_memory, verbose=False)
        

    def run_conversational_llm(self, prompt: str, output_parser: StructuredOutputParser=None):
        response = self.conversation_chain.predict(input=prompt)
        if output_parser:
            parsed_response = output_parser.parse(response)
            return parsed_response
        return response
    
    def run_normal_llm(self, prompt_template: PromptTemplate, output_parser: StructuredOutputParser = None, input_values: dict = {}):
        llm_chain = LLMChain(
            llm=self.llm_gpt_4, prompt=prompt_template)

        result = llm_chain.run(input_values)
        print('---Chain: ',result)
        if output_parser:
            return output_parser.parse(result)
        return result
