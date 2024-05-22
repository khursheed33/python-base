import requests
from typing import Any, List, Optional
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from app.utils.utility_manager import UtilityManager

class LocalLLMControlller(LLM, UtilityManager):
    """A custom chat model that makes a request to an endpoint with a specified payload."""
    
    def __init__(self):
        self.LLM_ENDPOINT = self.get_env_variable('LOCAL_LLM_URL')
        self.MAX_TOKENS = self.get_env_variable('LOCAL_LLM_MAX_TOKENS')
        self.TEMPERATURE = self.get_env_variable('LOCAL_LLM_TEMPERATURE')
        self.STREAM = self.get_env_variable('LOCAL_LLM_STEAM')

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
