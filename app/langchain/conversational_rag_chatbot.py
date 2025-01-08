from datetime import datetime
import logging
from typing import Any, Dict, List, Union
from langchain_core.documents import Document
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.callbacks import get_openai_callback
from app.utils.utility_manager import UtilityManager
from langchain_core.messages import HumanMessage, AIMessage
from langchain.vectorstores.pgvector import PGVector

class ConversationalRAGChatbot(UtilityManager):
    def __init__(self, llm: Any, vectorstore: PGVector, memory_window: int = 10):
        """Initializes the chatbot with an LLM and vectorstore for document retrieval."""
        self.__LLM = llm
        self.__VECTORSTORE = vectorstore
        self.__CONVERSATION_MEMORY: Dict[str, ConversationBufferWindowMemory] = {}
        self.memory_window = memory_window

    def chat(
        self, 
        query: str, 
        user_id: str = '33', 
        return_history: bool = False, 
        top_k: int = 5, 
        return_documents: bool = False, 
        relevancy: float = 0.5
    ) -> Dict[str, Any]:
        """
        Handles user query, retrieves relevant documents using PGVector, 
        and returns an answer based on chat history and retrieval chain.
        
        Args:
            query (str): The user query.
            user_id (str): The user identifier. Defaults to '33'.
            return_history (bool): Whether to return the chat history. Defaults to False.
            top_k (int): The number of top documents to retrieve. Defaults to 5.
            return_documents (bool): Whether to return the source documents. Defaults to False.
            relevancy (float): Multiplier for document relevancy. Defaults to 0.5.
        
        Returns:
            Dict[str, Any]: The chatbot's answer, source documents, tokens used, and more.
        """
        logging.info(f"Handling query for user_id: {user_id} with query: {query}")
        start_time = datetime.now()

        if user_id not in self.__CONVERSATION_MEMORY:
            self.__CONVERSATION_MEMORY[user_id] = ConversationBufferWindowMemory(
                memory_key='chat_history', 
                return_messages=True, 
                output_key='answer',
                k=self.memory_window,
            )

        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.__LLM,
            retriever=self.__VECTORSTORE.as_retriever(k=top_k, lambda_mult=relevancy),
            memory=self.__CONVERSATION_MEMORY[user_id],
            return_source_documents=True,
        )

        try:
            with get_openai_callback() as cb:
                response = conversation_chain({"question": query})
                total_time = self.calculate_response_time(start_time)

                docs: List[Document] = response['source_documents']
                chat_history: List[Union[HumanMessage, AIMessage]] = response['chat_history']
                
                sources = {doc.metadata['source'] for doc in docs}

                answer = {
                    "question": query,
                    "answer": response['answer'],
                    "sources": list(sources),
                    "documents": docs if return_documents else [],
                    "chat_history": chat_history if return_history else [],
                    "total_tokens": cb.total_tokens,
                    "completion_tokens": cb.completion_tokens,
                    "total_cost": cb.total_cost,
                    "prompt_tokens": cb.prompt_tokens,
                    "time_taken": total_time,
                }

                return answer

        except Exception as e:
            logging.error("Error during chat response generation: {}".format(str(e)))
            raise e

    def delete_chat_history(self, user_id: str) -> Dict[str, str]:
        """
        Deletes the chat history for a given user.

        Args:
            user_id (str): The user's identifier.

        Returns:
            Dict[str, str]: Message confirming deletion or user not found.
        """
        if user_id in self.__CONVERSATION_MEMORY:
            del self.__CONVERSATION_MEMORY[user_id]
            return {"message": "Chat history deleted."}
        else:
            return {"message": "User not found."}

    def get_chat_history(self, user_id: str) -> List[Dict[str, str]]:
        """
        Retrieves the chat history for a given user.

        Args:
            user_id (str): The user's identifier.

        Returns:
            List[Dict[str, str]]: List of human/AI message pairs.
        """
        if user_id in self.__CONVERSATION_MEMORY:
            messages: List[Union[HumanMessage, AIMessage]] = self.__CONVERSATION_MEMORY[user_id].buffer
            human_messages = [message for message in messages if isinstance(message, HumanMessage)]
            ai_messages = [message for message in messages if isinstance(message, AIMessage)]

            final_messages = [
                {"human": human_message.content, "ai": ai_message.content}
                for human_message, ai_message in zip(human_messages, ai_messages)
            ]

            return final_messages
        else:
            return []

