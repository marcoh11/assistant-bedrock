from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from llm_handler import LLMHandler
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Eres un asistente especializado en IA. Responde en 20 palabras o menos",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
runnable = prompt | LLMHandler.Bedrock()
with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

response = with_message_history.invoke(
    {"input": "Hola mi nombre es marco como estas"},
    config={"configurable": {"session_id": "abc123"}}
)

response = with_message_history.invoke(
    {"input": "Como?"},
    config={"configurable": {"session_id": "abc123"}}
)
print(response)