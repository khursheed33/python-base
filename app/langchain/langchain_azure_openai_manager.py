import os,re
from typing import Any
from langchain_community.chat_models import  AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain, LLMChain
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import  AzureOpenAIEmbeddings
from app.utils.utility_manager import UtilityManager
from app.enums.env_keys import EnvKeys


class LangchainOpenAIManager(UtilityManager):
    def __init__(
        self,STOP:Any = None, 
        MAX_RETRY:int = 1,
        MAX_TOKENS: int = -1,
        ):
        super().__init__()
        
        self.AZURE_OPENAI_KEY = self.get_env_variable(EnvKeys.AZURE_OPENAI_KEY.value)
        self.AZURE_TEMPERATURE = self.get_env_variable(EnvKeys.AZURE_OPENAI_TEMPERATURE.value)
        self.AZURE_MODEL = self.get_env_variable(EnvKeys.AZURE_OPENAI_MODEL.value)
        self.AZURE_BASE_URL = self.get_env_variable(EnvKeys.AZURE_OPENAI_BASE_URL.value)
        self.AZURE_DEPLOYMENT = self.get_env_variable(EnvKeys.AZURE_OPENAI_DEPLOYMENT.value)
        self.AZURE_VERSION = self.get_env_variable(EnvKeys.AZURE_OPENAI_API_VERSION.value)
        self.STOP = STOP
        self.MAX_RETRY = MAX_RETRY
        self.MAX_TOKENS = MAX_TOKENS
        
        os.environ["OPENAI_API_KEY"] = self.AZURE_OPENAI_KEY
        
        self.llm_model = AzureChatOpenAI(
            model_name=self.AZURE_MODEL,
            temperature=self.AZURE_TEMPERATURE,
            api_key=self.AZURE_OPENAI_KEY,
            api_version=self.AZURE_VERSION,
            azure_deployment=self.AZURE_DEPLOYMENT,
            azure_endpoint=self.AZURE_BASE_URL,
            stop=self.STOP,
        )

        # self.embedding = AzureOpenAIEmbeddings(openai_api_key=self.AZURE_OPENAI_KEY, chunk_size=2000)

        
        self.conversation_memory:ConversationBufferMemory = ConversationBufferMemory(
            llm=self.llm_model,)

        self.conversation_chain:ConversationChain = ConversationChain(
            llm=self.llm_model, memory=self.conversation_memory)

    def run_conversational_chain(self, prompt: str, output_parser: StructuredOutputParser = None, dont_store:bool = False) -> dict:
        """
        This LLM chain has memory, Chats will be stored by default.
        """
        response = self.conversation_chain.predict(input=prompt)
        if output_parser:
            response = output_parser.parse(response)
        
        if dont_store:
            # Remove last message from buffer
            self.clean_and_add_updated_message()
            
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
    
    def save_chat(self, question: str, response: str):
        return self.conversation_memory.save_context(inputs={'inputs': question}, outputs={'outputs': response})


    
    def clean_and_add_updated_message(self):
        # Define a regular expression pattern to match "Human: response" and "AI: response" pairs
        pattern = r'Human:(.*?)(?=Human:|AI:|$)AI:(.*?)(?=Human:|AI:|$)'
        all_messages = self.conversation_chain.memory.buffer
        # Find all matches of the pattern in the messages
        matches = re.findall(pattern, all_messages, re.DOTALL)

        # Check if there are any matches
        if matches:
            # Remove the last "Human: response" and "AI: response" pair
            matches.pop()

        # Clear the current buffer
        self.conversation_memory.clear()

        # Save the updated context back into the conversation memory
        for human_input, ai_output in matches:
            self.save_chat(question=human_input, response=ai_output)

