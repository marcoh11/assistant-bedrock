from fastapi import FastAPI
from pydantic import BaseModel
from conversation_manager import ConversationManager
from llm_handler import LLMHandler

app = FastAPI()
conversation_manager = ConversationManager()
llm_handler = LLMHandler()

class Message(BaseModel):
    content: str

@app.post("/conversation/create")
async def create_conversation():
    conversation_id = conversation_manager.create_conversation()
    return {"conversation_id": conversation_id}

@app.post("/conversation/{conversation_id}/message")
async def add_message(conversation_id: str, message: Message):
    conversation = conversation_manager.get_conversation(conversation_id)
    if not conversation:
        return {"error": "Conversation not found"}
    conversation_manager.add_message(conversation_id, "user", message.content)
    response = llm_handler.generate_response(conversation.messages)
    conversation_manager.add_message(conversation_id, "assistant", response)
    #Aca llamar a llm_handler pero debo modificar en el conversation_manager
    #conversation_manager.format_messages(conversation.messages)
    return {"response": response}