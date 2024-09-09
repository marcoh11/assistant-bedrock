from uuid import uuid4
from typing import Dict, List
from prompts import INITIAL_PROMPT 

class Conversation:
    def __init__(self):
        self.messages: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}

    def create_conversation(self) -> str:
        conversation_id = str(uuid4())
        conversation=Conversation()
        conversation.add_message("system",INITIAL_PROMPT)
        self.conversations[conversation_id] = conversation
        
        return conversation_id

    def get_conversation(self, conversation_id: str) -> Conversation:
        return self.conversations.get(conversation_id)

    def add_message(self, conversation_id: str, role: str, content: str):
        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.add_message(role, content)

    def estimate_tokens(self, texts):
        total_tokens = sum(len(text) / 4 for text in texts)
        print("total tokens:",total_tokens)
        return total_tokens
    def regenerate_conversation():
        return None
    def format_messages(self, messages: List[Dict[str, str]]) -> str:
        formatted_messages = []
        for message in messages:
            if message["role"] == "system":
                formatted_messages.append(f"system: {message['content']}")
            elif message["role"] == "user":
                formatted_messages.append(f"user: {message['content']}")
            elif message["role"] == "assistant":
                formatted_messages.append(f"assistant: {message['content']}")
        if self.estimate_tokens(formatted_messages)>4000:
            self.regenerate_conversation()
        print(messages[0])
        formatted_messages.append("assistant:")
        print(type(formatted_messages[0]))