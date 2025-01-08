import os
from typing import List, Dict, Optional
from typing_extensions import NotRequired, TypedDict
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import groq


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
        # Add nodes
        self.workflow.add_node("process", self._process_message)

        # Add edges
        self.workflow.set_entry_point("process")
        self.workflow.add_conditional_edges(
            "process", lambda x: x["next_node"], {None: END}
        )

        # Compile the workflow
        self.app = self.workflow.compile()

    def invoke_workflow(self, state: GraphState) -> GraphState:
        return self.app.invoke(state)


# Main Application
class ChatApplication:
    def __init__(self, workflow_manager: WorkflowManager):
        self.workflow_manager = workflow_manager

    def process_input(self, user_input: str) -> str:
        initial_state = {
            "messages": [{"role": "user", "content": user_input}],
            "next_node": "",
            "response": "",
        }
        final_state = self.workflow_manager.invoke_workflow(initial_state)
        return final_state["response"]

    def run(self, inputs: List[str]) -> None:
        for input_text in inputs:
            print(f"\nInput: {input_text}")
            print(f"Response: {self.process_input(input_text)}")


if __name__ == "__main__":
    # Load configuration
    EnvironmentConfig.load_env_file()
    groq_api_key = EnvironmentConfig.get_env_variable("GROQ_API_KEY")

    # Initialize components
    groq_client = GroqClient(api_key=groq_api_key)
    workflow_manager = WorkflowManager(groq_client=groq_client)
    chat_app = ChatApplication(workflow_manager=workflow_manager)

    # Run the application
    example_inputs = [
        "What is the derivative of x^2?",
        "What are the symptoms of flu?",
        "How does photosynthesis work?",
        "Explain Newton's laws",
        "What's your favorite color?",
    ]
    chat_app.run(example_inputs)
