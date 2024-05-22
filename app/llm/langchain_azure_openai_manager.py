import os,re
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationChain, LLMChain
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import OpenAIEmbeddings
from app.llm.user_conversation_memory import UserConversationMemory
from app.utils.utility_manager import UtilityManager
from app.enums.env_keys import EnvKeys


class LangchainOpenAIManager(UtilityManager):
    def __init__(self):
        super().__init__()
        
        self.OPENAI_KEY = self.get_env_variable(EnvKeys.APP_OPENAI_KEY.value)
        self.TEMPERATURE = self.get_env_variable(EnvKeys.APP_OPENAI_TEMPERATURE.value)
        self.MODEL = self.get_env_variable(EnvKeys.APP_OPENAI_MODEL.value)
        self.OPENAI_VERBOSE = self.get_env_variable(EnvKeys.APP_OPENAI_VERBOSE.value)
        
        os.environ["OPENAI_API_KEY"] = self.OPENAI_KEY
        
        self.llm_model = ChatOpenAI(
            model_name=self.MODEL,
            temperature=self.TEMPERATURE
        )

        self.embedding = OpenAIEmbeddings(openai_api_key=self.OPENAI_KEY, chunk_size=2000)

        


    def run_conversational_chain(self, prompt: str, output_parser: StructuredOutputParser = None, dont_store:bool = False) -> dict:
        """
        This LLM chain has memory, Chats will be stored by default.
        """
        self.conversation_memory = UserConversationMemory(
            llm=self.llm_model,)

        self.conversation_chain:ConversationChain = ConversationChain(
            llm=self.llm_model, memory=self.conversation_memory, verbose=self.OPENAI_VERBOSE)
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

