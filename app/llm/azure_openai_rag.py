from app.enums.env_keys import EnvKeys
from app.llm.langchain_azure_openai_manager import LangchainOpenAIManager
from app.utils.utility_manager import UtilityManager
import os
import openai

class AzureOpenAIRAG(UtilityManager):
    def __init__(self):
        pass
    
    
    def run_chain(self):
        # AZURE_OPENAI_KEY
        AZURE_OPENAI_KEY= self.get_env_variable(EnvKeys.AZURE_OPENAI_KEY.value)
        # AZURE_OPENAI_MODEL
        AZURE_OPENAI_MODEL= self.get_env_variable(EnvKeys.AZURE_OPENAI_MODEL.value)
        # AZURE_OPENAI_TEMPERATURE
        AZURE_OPENAI_TEMPERATURE= self.get_env_variable(EnvKeys.AZURE_OPENAI_TEMPERATURE.value)
        # AZURE_OPENAI_DEPLOYMENT
        AZURE_OPENAI_DEPLOYMENT= self.get_env_variable(EnvKeys.AZURE_OPENAI_DEPLOYMENT.value)
        # AZURE_OPENAI_BASE_URL
        AZURE_OPENAI_BASE_URL= self.get_env_variable(EnvKeys.AZURE_OPENAI_BASE_URL.value)
        # AZURE_OPENAI_API_VERSION
        AZURE_OPENAI_API_VERSION= self.get_env_variable(EnvKeys.AZURE_OPENAI_API_VERSION.value)
        # Used by the OpenAI SDK
        openai.api_type = 'azure'
        openai.api_key = AZURE_OPENAI_KEY
        openai.api_version = AZURE_OPENAI_API_VERSION
        openai.azure_endpoint = AZURE_OPENAI_BASE_URL
        
        
        prompt_prefix = """<|im_start|>system
        Assistant helps the company employees with their healthcare plan questions and employee handbook questions. 
        Answer ONLY with the facts listed in the list of sources below. If there isn't enough information below, say you don't know. Do not generate answers that don't use the sources below. If asking a clarifying question to the user would help, ask the question. 
        Each source has a name followed by colon and the actual information, always include the source name for each fact you use in the response. Use square brakets to reference the source, e.g. [info1.txt]. Don't combine sources, list each source separately, e.g. [info1.txt][info2.pdf].

        Sources:
        {sources}

        <|im_end|>"""

        turn_prefix = """
        <|im_start|>user
        """

        turn_suffix = """
        <|im_end|>
        <|im_start|>assistant
        """

        prompt_history = turn_prefix

        history = []

        summary_prompt_template = """Below is a summary of the conversation so far, and a new question asked by the user that needs to be answered by searching in a knowledge base. Generate a search query based on the conversation and the new question. Source names are not good search terms to include in the search query.

        Summary:
        {summary}

        Question:
        {question}

        Search query:
        """
        # Execute this cell multiple times updating user_input to accumulate chat history
        user_input = "Does my plan cover annual eye exams?"

        # Exclude category, to simulate scenarios where there's a set of docs you can't see
        exclude_category = None
        model = LangchainOpenAIManager(STOP=["\n"])
        
        if len(history) > 0:
            
            completion = model.run_conversational_chain(
                prompt=summary_prompt_template.format(summary="\n".join(history), question=user_input),
                dont_store=True,
            )
            search = completion['response']
        else:
            search = user_input

        # Alternatively simply use search_client.search(q, top=3) if not using semantic search
        print("Searching:", search)
        print("-------------------")
        filter = "category ne '{}'".format(exclude_category.replace("'", "''")) if exclude_category else None
        content = "retreived contents (RAG)"

        prompt = prompt_prefix.format(sources=content) + prompt_history + user_input + turn_suffix
        
        model = LangchainOpenAIManager(STOP=["<|im_end|>", "<|im_start|>"])
        
        completion = model.run_conversational_chain(
                prompt=summary_prompt_template.format(summary="\n".join(history), question=user_input),
                dont_store=True,
            )
        
        prompt_history += user_input + turn_suffix + completion['response'] + "\n<|im_end|>" + turn_prefix
        history.append("user: " + user_input)
        history.append("assistant: " + completion['response'])

        print("\n-------------------\n".join(history))
        print("\n-------------------\nPrompt:\n" + prompt)
        return prompt_history
    
    