import boto3
from langchain_aws import BedrockLLM,ChatBedrock
from typing import List, Dict
import json

class LLMHandler:
    def __init__(self):
        bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-east-1")
        self.llm = BedrockLLM(
            client=bedrock_runtime,
            model_id="mistral.mixtral-8x7b-instruct-v0:1", 
            model_kwargs={"temperature": 0.3,
                          "max_tokens": 500
                         }
        )
        self.claude = ChatBedrock(
            client=bedrock_runtime,
            model_id="anthropic.claude-3-haiku-20240307-v1:0", 
            model_kwargs=dict(temperature=0.2)
        )
        self.llm_summary = BedrockLLM(
            client=bedrock_runtime,
            model_id="mistral.mixtral-8x7b-instruct-v0:1", 
            model_kwargs={"temperature": 0.3}
        )
        self.llm_embedding = BedrockLLM(
            client=bedrock_runtime,
            model_id="mistral.mixtral-8x7b-instruct-v0:1", 
            model_kwargs={"temperature": 0.3}
        )
    
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        formatted_prompt = self.format_messages(messages)
        #print(formatted_prompt)
        response = self.claude.invoke(formatted_prompt)
        #print(response) 
        return response

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

    def format_messages_json(self, messages: List[Dict[str, str]]) -> str:
        messages.append({'role': 'assistant','content':''})
        return json.dumps(messages)