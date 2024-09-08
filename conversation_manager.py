from uuid import uuid4
from typing import Dict
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage
from llm_handler import LLMHandler
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables import RunnableParallel


class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, RunnableWithMessageHistory] = {}
        self.memories: Dict[str, ChatMessageHistory] = {}
        self.llm = RunnableParallel({"output_message": LLMHandler.Bedrock()})

    def get_session_history(self,session_id: str) -> BaseChatMessageHistory:
        try:
            print("historias: ",self.memories[session_id])
        except KeyError:
            print(f"Session ID {session_id} not found in memories.")
        if session_id not in self.memories:
            self.memories[session_id] = ChatMessageHistory()
            print("ides update:")
        return self.memories[session_id]
    
    def create_conversation(self) -> str:
        conversation_id = "abc123"
        print("Inicalizacion primera vez con id:",conversation_id)
        prompt = ChatPromptTemplate.from_messages([
            (
            "system",
            "Eres un asistente especializado en IA. Responde en 20 palabras o menos",
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])
        runnable = prompt | self.llm
        self.conversations[conversation_id] = RunnableWithMessageHistory(
            runnable,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="history",
            history_factory_config=[
                ConfigurableFieldSpec(
                    id="conversation_id",
                    annotation=str,
                    name="Conversation ID",
                    description="Unique identifier for the conversation.",
                )
            ]
        )
        print("finalizacion create")
        return conversation_id
    
    
    def get_conversation(self, conversation_id: str) -> RunnableWithMessageHistory:
        return self.conversations[conversation_id]
    
    def generate_response(self, conversation_id: str, message: str) -> str:
        conversation = self.get_conversation(conversation_id)
        #print("conv: ",conversation)
        if conversation:
            try:
                print(f"Sending to model: {message}")
                response = conversation.invoke(
                    {"input":message},
                    config={"configurable": {"conversation_id": conversation_id}}
                )
                response= response['output_message'].replace('\nBot: ', '').strip()
                print(f"Raw response from model: {response}",type(response)) 
                return response
            except Exception as e:
                print(f"Error generating response: {e}")
                return f"Error: Failed to generate response. Details: {str(e)}"
        return "Error: Conversation not found"

    def get_conversation_histories(self, conversation_id: str):
        conversation = self.get_conversation(conversation_id)
        if conversation:
            return conversation.get_session_history(conversation_id)
        return []