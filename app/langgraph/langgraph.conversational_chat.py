import os
from typing import List, Dict, Optional
from typing_extensions import NotRequired, TypedDict
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import groq
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from uuid import uuid4


# Load environment variables
class EnvironmentConfig:
    @staticmethod
    def load_env_file(file_name: str = ".env") -> None:
        load_dotenv(file_name)

    @staticmethod
    def get_env_variable(key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"{key} environment variable is not set")
        return value


# Message and State type definitions
class Message(TypedDict):
    role: str
    content: str


class GraphState(TypedDict):
    messages: List[Message]
    next_node: NotRequired[str]
    response: NotRequired[str]


# API Models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str


# GROQ client wrapper
class GroqClient:
    def __init__(self, api_key: str):
        self.client = groq.Groq(api_key=api_key)

    def get_chat_completion(self, messages: List[Message], model: str) -> str:
        response = self.client.chat.completions.create(
            messages=[{"role": m["role"], "content": m["content"]} for m in messages],
            model=model,
        )
        return response.choices[0].message.content


# Conversation Manager
class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, List[Message]] = {}

    def create_conversation(self) -> str:
        conversation_id = str(uuid4())
        self.conversations[conversation_id] = []
        return conversation_id

    def get_conversation(self, conversation_id: str) -> List[Message]:
        if conversation_id not in self.conversations:
            raise ValueError(f"Conversation {conversation_id} not found")
        return self.conversations[conversation_id]

    def add_message(self, conversation_id: str, message: Message) -> None:
        if conversation_id not in self.conversations:
            raise ValueError(f"Conversation {conversation_id} not found")
        self.conversations[conversation_id].append(message)


# StateGraph Workflow Manager
class WorkflowManager:
    def __init__(self, groq_client: GroqClient):
        self.groq_client = groq_client
        self.workflow = StateGraph(GraphState)
        self._configure_workflow()

    def _process_message(self, state: GraphState) -> GraphState:
        messages = state["messages"]
        response = self.groq_client.get_chat_completion(
            messages=messages, model="mixtral-8x7b-32768"
        )
        return {
            "messages": messages,
            "response": response,
            "next_node": None,  # Stops the workflow
        }

    def _configure_workflow(self) -> None:
        self.workflow.add_node("process", self._process_message)
        self.workflow.set_entry_point("process")
        self.workflow.add_conditional_edges(
            "process", lambda x: x["next_node"], {None: END}
        )
        self.app = self.workflow.compile()

    def invoke_workflow(self, state: GraphState) -> GraphState:
        return self.app.invoke(state)


# Chat Application with FastAPI
class ChatApplication:
    def __init__(self, workflow_manager: WorkflowManager):
        self.workflow_manager = workflow_manager
        self.conversation_manager = ConversationManager()
        self.api = FastAPI(title="Conversational Chatbot API")
        self._configure_routes()

    def _configure_routes(self) -> None:
        @self.api.post("/chat", response_model=ChatResponse)
        async def chat(request: ChatRequest) -> ChatResponse:
            try:
                # Get or create conversation
                conversation_id = request.conversation_id or self.conversation_manager.create_conversation()
                
                # Get conversation history
                conversation = self.conversation_manager.get_conversation(conversation_id)
                
                # Add user message to conversation
                user_message = {"role": "user", "content": request.message}
                conversation.append(user_message)
                
                # Process message through workflow
                state = {
                    "messages": conversation,
                    "next_node": "",
                    "response": "",
                }
                final_state = self.workflow_manager.invoke_workflow(state)
                
                # Add assistant response to conversation
                assistant_message = {"role": "assistant", "content": final_state["response"]}
                conversation.append(assistant_message)
                
                return ChatResponse(
                    response=final_state["response"],
                    conversation_id=conversation_id
                )
            
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.api.get("/conversations/{conversation_id}")
        async def get_conversation(conversation_id: str) -> List[Message]:
            try:
                return self.conversation_manager.get_conversation(conversation_id)
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))

    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        uvicorn.run(self.api, host=host, port=port)


if __name__ == "__main__":
    # Load configuration
    EnvironmentConfig.load_env_file()
    groq_api_key = EnvironmentConfig.get_env_variable("GROQ_API_KEY")

    # Initialize components
    groq_client = GroqClient(api_key=groq_api_key)
    workflow_manager = WorkflowManager(groq_client=groq_client)
    chat_app = ChatApplication(workflow_manager=workflow_manager)

    # Run the application
    chat_app.run()