from datetime import datetime
from typing import Any, Dict, List
from venv import logger
from langchain_core.documents import Document
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.callbacks import get_openai_callback
from app.utils.utility_manager import UtilityManager
from langchain_core.messages import HumanMessage, AIMessage
from langchain.vectorstores.pgvector import PGVector

class ConversationalRAGChatbot(UtilityManager):
    def __init__(self, llm:Any, vectorstore: PGVector):
        self.__LLM = llm
        self.__VECTORSTORE = vectorstore
    
        self.__CONVERSATION_MEMORY: Dict[str, ConversationBufferWindowMemory] = {}

    def chat(self, query: str,user_id: str = '33', return_history: bool = False, top_k:int = 3, return_documents: bool = False) -> Dict[str, Any]:
        logger.info("Handling query for user_id: {} with query: {}".format(user_id, query))
        start_time = datetime.now()
        if user_id not in self.__CONVERSATION_MEMORY:
            self.__CONVERSATION_MEMORY[user_id] = ConversationBufferWindowMemory(
        memory_key='chat_history', return_messages=True, output_key='answer')

        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.__LLM,
            retriever=self.__VECTORSTORE.as_retriever(),
            memory=self.__CONVERSATION_MEMORY[user_id],
            return_source_documents=True,
        )
        
        try:
            with get_openai_callback() as cb:
                response = conversation_chain({"question": query})
                total_time = self.calculate_response_time(start_time)
                docs:List[Document] = response['source_documents']
                chat_history: List[HumanMessage,AIMessage] = response['chat_history']
                sources:set = set()
                for doc in docs:
                    source = doc.metadata['source']
                    sources.add(source)
                
                answer = {
                    "question": query,
                    "answer": response['answer'],
                    "sources": sources,
                    "documents": docs if return_documents else [],
                    "chat_history": chat_history if return_history else [],
                    "total_tokens": cb.total_tokens,
                    "completion_tokens":cb.completion_tokens,
                    "total_cost": cb.total_cost,
                    "prompt_tokens":cb.prompt_tokens,
                    "time_taken":total_time,
                    }
                return answer
        except Exception as e:
            logger.error(f"Error in get_response: {str(e)}")
            print("Error: ", str(e))
            raise

    def delete_chats(self, user_id: str) -> Dict[str, str]:
        if user_id in self.__CONVERSATION_MEMORY:
            del self.__CONVERSATION_MEMORY[user_id]
            return {"message": "Deleted"}  
        else:
            return {"message": "User not found"}

    def get_chat_history(self, user_id: str) -> List[Dict[str, str]]:
        if user_id in self.__CONVERSATION_MEMORY:
            messages:List[HumanMessage,AIMessage] = self.__CONVERSATION_MEMORY[user_id].buffer
            print("ALL: ", messages)
            human_messages = [message for message in messages if isinstance(message, HumanMessage)]
            ai_messages = [message for message in messages if isinstance(message, AIMessage)]
            final_messages = [{"human": str(human_message.content), "ai": str(ai_message.content)} for human_message, ai_message in zip(human_messages, ai_messages)]
            return final_messages
        else:
            return []
