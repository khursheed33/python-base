
from app.controllers.local_llm.local_llm_controller import LocalLLMControlller
from app.utils.utility_manager import UtilityManager
from langchain.chains import ConversationChain, LLMChain
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import PromptTemplate
from app.enums.env_keys import EnvKeys
from app.llm.user_conversation_memory import UserConversationMemory
from dotenv import load_dotenv

load_dotenv()



class LocalLLMManager(UtilityManager):
    def __init__(self, memory:UserConversationMemory):
        super().__init__()
        
        self.TEMPERATURE = int(self.get_env_variable(EnvKeys.LOCAL_LLM_TEMPERATURE.value))
        self.MAX_TOKENS = int(self.get_env_variable(EnvKeys.LOCAL_LLM_MAX_TOKENS.value))
        self.STREAM = self.get_env_variable(EnvKeys.LOCAL_LLM_STEAM.value)
        self.OPENAI_VERBOSE = self.get_env_variable(EnvKeys.APP_OPENAI_VERBOSE.value)
        
        self.llm_model = LocalLLMControlller()

        self.conversation_memory = memory
        
        self.conversation_chain = ConversationChain(
            llm=self.llm_model, 
            memory=self.conversation_memory,
            verbose=self.OPENAI_VERBOSE,
            )

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
            llm=self.llm_model,
            prompt=prompt_template,
        )

        result = llm_chain.run(input_values)

        if output_parser:
            return output_parser.parse(result)

        return {"response": result}
        
