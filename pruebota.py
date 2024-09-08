
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from llm_handler import LLMHandler

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Eres un asistente especializado en IA. Responde en 20 palabras o menos",
        ),
        #MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
runnable = prompt | LLMHandler.Bedrock()

print(runnable.invoke( {"input":"Cual es el futuro de la IA"},
                    config={"configurable": {"conversation_id": "abc123"}}
))