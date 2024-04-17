import os
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain, LLMChain
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import PromptTemplate
from app.utils.utility_manager import UtilityManager
from app.enums.env_keys import EnvKeys


class LangchainOpenAIManager(UtilityManager):
    def __init__(self):
        super().__init__()
        self.OPENAI_KEY = self.get_env_variable(EnvKeys.APP_OPENAI_KEY.value)
        self.TEMPERATURE = self.get_env_variable(
            EnvKeys.APP_OPENAI_TEMPERATURE.value)
        self.llm_model = ChatOpenAI(
            model_name=self.OPENAI_KEY,
            temperature=self.TEMPERATURE
        )

        self.conversation_memory = ConversationBufferMemory(
            llm=self.llm_model)

        self.conversation_chain = ConversationChain(
            llm=self.llm_model, memory=self.conversation_memory, verbose=False)

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
