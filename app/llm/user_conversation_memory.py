from langchain.memory import ConversationBufferWindowMemory
from langchain_core.memory import BaseMemory

class UserConversationMemory(BaseMemory):
    _instance = None
    _user_memories = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserConversationMemory, cls).__new__(cls)
        return cls._instance

    def __init__(self, llm_model, user_id: str = None, window_size: int = 10) -> None:
        if user_id not in self._user_memories:
            self.user_id = user_id
            self.window_size = window_size
            self.llm_model = llm_model
            self.conversation_memory = self.create_conversation_memory()
            self._user_memories[user_id] = self.conversation_memory
        else:
            self.conversation_memory = self._user_memories[user_id]

    def create_conversation_memory(self):
        return ConversationBufferWindowMemory(
            llm=self.llm_model,
            window_size=self.window_size
        )

    def __getattr__(self, name):
        """Delegate attribute access to the conversation_memory instance."""
        return getattr(self.conversation_memory, name)
