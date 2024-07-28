import os
import logging
from typing import Any, Dict, List
from venv import logger

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks import get_openai_callback
from app.utils.utility_manager import UtilityManager
from langchain_core.messages import HumanMessage, AIMessage
class ConversationalRAGChatbot(UtilityManager):
    def __init__(self, llm:Any, vectorstore:Any):
        self.__LLM = llm
        self.__VECTORSTORE = vectorstore
        
        # Conversation memory
        self.__CONVERSATION_MEMORY: Dict[str, ConversationBufferMemory] = {}

    def chat(self, query: str,user_id: str = '33', return_history: bool = False) -> Dict[str, Any]:
        logger.info(f"Handling query for user_id: {user_id} with query: {query}")

        if user_id not in self.__CONVERSATION_MEMORY:
            self.__CONVERSATION_MEMORY[user_id] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.__LLM,
            retriever=self.__VECTORSTORE.as_retriever(),
            memory=self.__CONVERSATION_MEMORY[user_id]
        )

        try:
            relevant_docs = self.__VECTORSTORE.similarity_search(query, k=3)
            
            if not relevant_docs:
                return {
                    "answer": "I'm sorry, but this query is out of scope for my knowledge base.",
                    "question": query,
                    "history": []
                }

            with get_openai_callback() as cb:
                response = conversation_chain({"question": query})
            messages  = self.get_chat_history(user_id=user_id)
            if "I don't have enough information to answer that question" in response['answer']:
                if return_history:
                    
                    return {
                        "answer": "This query requires escalation. No specific answer found in the documents.",
                        "question": query,
                        "history": messages
                    }
                else:
                    return {
                        "answer": "This query requires escalation. No specific answer found in the documents.",
                        "question": query
                    }

            if return_history:
                return {
                    "answer": response['answer'],
                    "question": query,
                    "history": messages
                }
            else:
                return {
                    "answer": response['answer'],
                    "question": query
                }
        except Exception as e:
            logger.error(f"Error in get_response: {str(e)}")
            raise

    def delete_chats(self, user_id: str) -> Dict[str, str]:
        if user_id in self.__CONVERSATION_MEMORY:
            del self.__CONVERSATION_MEMORY[user_id]
            return {"message": "Deleted"}
        else:
            return {"message": "User not found"}

    def get_chat_history(self, user_id: str) -> List[Dict[str, str]]:
        if user_id in self.__CONVERSATION_MEMORY:
            messages = self.__CONVERSATION_MEMORY[user_id].buffer.get_messages()
            human_messages = [message for message in messages if isinstance(message, HumanMessage)]
            ai_messages = [message for message in messages if isinstance(message, AIMessage)]
            return [{"human": str(human_message), "ai": str(ai_message)} for human_message, ai_message in zip(human_messages, ai_messages)]
        else:
            return []