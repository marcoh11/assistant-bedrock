import boto3
from langchain_aws import BedrockLLM
from typing import List, Dict

class LLMHandler:
    def __init__(self):
        bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-east-1")
        self.llm = BedrockLLM(
            client=bedrock_runtime,
            model_id="mistral.mixtral-8x7b-instruct-v0:1", 
            model_kwargs={"temperature": 0.3,
                          "max_tokens": 80,
                          "top_p": 0.8,}
        )
        self.llc = BedrockLLM(
            client=bedrock_runtime,
            model_id="mistral.mixtral-8x7b-instruct-v0:1", 
            model_kwargs={"temperature": 0.3}
        )
    
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        formatted_prompt = self.format_messages(messages)
        response = self.llm.invoke(formatted_prompt)
        return response
        #return formatted_prompt

    def format_messages(self, messages: List[Dict[str, str]]) -> str:
        formatted_messages = []
        for message in messages:
            if message["role"] == "system":
                formatted_messages.append(f"system: {message['content']}")
            elif message["role"] == "user":
                formatted_messages.append(f"user: {message['content']}")
            elif message["role"] == "assistant":
                formatted_messages.append(f"assistant: {message['content']}")
        formatted_messages.append("assistant:")
        return  "\n".join(formatted_messages)