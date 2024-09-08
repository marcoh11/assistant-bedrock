import boto3
from langchain_aws import BedrockLLM

class LLMHandler:
    def Bedrock():
        bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-east-1")
        llm = BedrockLLM(
            client=bedrock_runtime,
            model_id="amazon.titan-text-express-v1",
            model_kwargs={"temperature": 0.2
                          }
        )
        return llm