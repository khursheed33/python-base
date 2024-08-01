import json
import os
import requests
from typing import Any, List, Optional
from langchain.memory import ConversationBufferMemory
from langchain_core.language_models.llms import LLM
from langchain.chains import ConversationChain, LLMChain
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from app.utils.utility_manager import UtilityManager
from app.enums.env_keys import EnvKeys
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class GROQLLM(LLM, UtilityManager):
    GROQ_API_KEY = os.getenv(EnvKeys.GROQ_API_KEY.value)
    MODEL = os.getenv(EnvKeys.GROQ_MODEL.value)
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        
        """Run the LLM on the given input by making a request to the GROQ API."""
        try:
                
            groq_client = Groq(
                api_key=self.GROQ_API_KEY,
            )
            
            chat_completion = groq_client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content":"Your an excellent assistant" ,
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model=self.MODEL,
                    )
            response_data = json.loads(chat_completion.model_dump_json())
            message_content = response_data["choices"][0]["message"]["content"]
            # total_tokens = response_data["usage"]["total_tokens"]
            # total_time = response_data["usage"]["total_time"]
            return message_content
        
        except requests.exceptions.RequestException as e:
                return f"Request failed: {e}"
        except (ValueError, KeyError) as e:
            return f"Error processing response: {e}"

        
    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        return "GROQ"

class LangchainGroqManager(UtilityManager):
    def __init__(self):
        super().__init__()
        
        self.TEMPERATURE = float(self.get_env_variable(EnvKeys.GROQ_TEMPERATURE.value))
        self.GROQ_VERBOSE = self.get_env_variable(EnvKeys.GROQ_VERBOSE.value)
        
        self.llm_model = GROQLLM()
        
        self.conversation_memory = ConversationBufferMemory(llm=self.llm_model)

        self.conversation_chain = ConversationChain(
            llm=self.llm_model, memory=self.conversation_memory, verbose=self.GROQ_VERBOSE)

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
