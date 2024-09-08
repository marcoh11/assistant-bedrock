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
            model_kwargs={"temperature": 0.3}
        )
        self.llc = BedrockLLM(
            client=bedrock_runtime,
            model_id="mistral.mixtral-8x7b-instruct-v0:1", 
            model_kwargs={"temperature": 0.3}
        )
        
    def estimate_tokens(self,text):
        return len(text) / 4
    
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        formatted_prompt = self.format_messages(messages)
        #response = self.llm.invoke(formatted_prompt)
        #return response
        return "formatted_prompt"
    
    def regenerate_history(self,history):
        print("Exediste los limites papu..")
        return "Exediste"
    

    def format_messages(self, messages: List[Dict[str, str]]) -> str:
        formatted_messages = []
        for message in messages:
            if message["role"] == "user":
                formatted_messages.append(f"Human: {message['content']}")
            elif message["role"] == "assistant":
                formatted_messages.append(f"Assistant: {message['content']}")
        formatted_messages.append("Assistant:")
        print( "\n".join(formatted_messages))