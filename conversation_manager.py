from uuid import uuid4
from typing import Dict, List

class Conversation:
    def __init__(self):
        self.messages: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}

    def create_conversation(self) -> str:
        print("Conversacion creada")
        conversation_id = str(uuid4())
        self.conversations[conversation_id] = Conversation()
        return conversation_id

    def get_conversation(self, conversation_id: str) -> Conversation:
        print("get_conversation")
        return self.conversations.get(conversation_id)

    def add_message(self, conversation_id: str, role: str, content: str):
        print("adding_message")
        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.add_message(role, content)
        
    
    def format_messages(self, messages: List[Dict[str, str]]) -> str:
        print("formating_message")
        formatted_messages = []
        for message in messages:
            if message["role"] == "user":
                formatted_messages.append(f"Human: {message['content']}")
            elif message["role"] == "assistant":
                formatted_messages.append(f"Assistant: {message['content']}")
        formatted_messages.append("Assistant:")
        print("\n".join(formatted_messages))