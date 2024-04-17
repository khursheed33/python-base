from app.llm.langchain_openai_manager import LangchainOpenAIManager

class LLMInstanceManager:
    def __init__(self):
        self.instances = {}

    def create_instance(self, user_id, conversation_id):
        # Create a new instance of MyClass
        instance = LangchainOpenAIManager()   
        
        # Check if user_id exists in instances dictionary
        if user_id not in self.instances:
            # If user_id does not exist, create a new dictionary entry
            self.instances[user_id] = {}

        # Add the new instance to the dictionary under user_id and conversation_id
        self.instances[user_id][conversation_id] = instance
        
        return self.get_instance(user_id=user_id,conversation_id=conversation_id)

    def get_instance(self, user_id, conversation_id) -> LangchainOpenAIManager:
        # Retrieve instance from the dictionary
        return self.instances.get(user_id, {}).get(conversation_id, None)

