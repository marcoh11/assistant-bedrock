from fastapi import FastAPI
from pydantic import BaseModel
from conversation_manager import ConversationManager
from llm_handler import LLMHandler
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI()

conversation_manager = ConversationManager()


class Message(BaseModel):
    content: str

@app.post("/conversation/create")
async def create_conversation():
    conversation_id = conversation_manager.create_conversation()
    return {"conversation_id": conversation_id}

@app.post("/conversation/{conversation_id}/message")
async def add_message(conversation_id: str, message: Message):
    response = conversation_manager.generate_response(conversation_id, message.content)
    return {"response": response}

@app.get("/conversation/{conversation_id}/history")
async def get_history(conversation_id: str):
    history = conversation_manager.get_conversation_history(conversation_id)
    return {"history": [{"role": "human" if isinstance(msg, HumanMessage) else "ai", "content": msg.content} for msg in history]}

@app.post("/conversation/{conversation_id}/reset")
async def reset_conversation(conversation_id: str):
    conversation_manager.create_conversation()
    return {"message": "Conversation reset successfully"}

@app.get("/conversation/{conversation_id}/debug")
async def debug_conversation(conversation_id: str):
    conversation = conversation_manager.get_conversation(conversation_id)
    if conversation:
        history = conversation.get_session_history(conversation_id)
        return {"history": [{"role": "human" if isinstance(msg, HumanMessage) else "ai", "content": msg.content} for msg in history]}
    return {"error": "Conversation not found"}
