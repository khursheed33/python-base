import os, requests, re
from app.utils.utility_manager import UtilityManager
from typing import Any, Dict, Iterator, List, Optional
from langchain.memory import ConversationBufferMemory
from langchain_core.language_models.llms import LLM
from langchain.chains import ConversationChain, LLMChain
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from app.enums.env_keys import EnvKeys
from dotenv import load_dotenv

load_dotenv()


class LocalLLM(LLM, UtilityManager):
    """A custom chat model that makes a request to an endpoint with a specified payload."""
    
    LLM_ENDPOINT = os.environ['LOCAL_LLM_URL']
    MAX_TOKENS = os.environ['LOCAL_LLM_MAX_TOKENS']
    TEMPERATURE = os.environ['LOCAL_LLM_TEMPERATURE']
    STREAM = os.environ['LOCAL_LLM_STEAM']
    
 

    def _call(
    self,
    prompt: str,
    stop: Optional[List[str]] = None,
    run_manager: Optional[CallbackManagerForLLMRun] = None,
    **kwargs: Any,
) -> str:
        
        """Run the LLM on the given input by making a request to an endpoint."""
        
        payload = {
            "messages": [
                {"role": "system", "content": "you are helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.TEMPERATURE,
            "max_tokens": self.MAX_TOKENS,
            "stream": self.STREAM,
        }
        try:
            response = requests.post(self.LLM_ENDPOINT, json=payload)
            response.raise_for_status()
            response_data = response.json()
            return response_data['choices'][0]['message']['content'].strip()
        except requests.exceptions.RequestException as e:
            return f"Request failed: {e}"
        except (ValueError, KeyError) as e:
            return f"Error processing response: {e}"
        
    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        # Return a descriptive string for your custom LLM
        return "custom"


class LocalLLMManager(UtilityManager):
    def __init__(self):
        super().__init__()
        
        self.TEMPERATURE = int(self.get_env_variable(EnvKeys.LOCAL_LLM_TEMPERATURE.value))
        self.MAX_TOKENS = int(self.get_env_variable(EnvKeys.LOCAL_LLM_MAX_TOKENS.value))
        self.STREAM = self.get_env_variable(EnvKeys.LOCAL_LLM_STREAM.value)
        self.OPENAI_VERBOSE = self.get_env_variable(EnvKeys.LOCAL_LLM_VERBOSE.value)
        
        self.llm_model = LocalLLM()
        
        self.conversation_memory = ConversationBufferMemory(
            llm=self.llm_model)

        self.conversation_chain = ConversationChain(
            llm=self.llm_model, memory=self.conversation_memory, verbose=self.OPENAI_VERBOSE)

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

        
