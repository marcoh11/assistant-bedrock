import boto3
import json

bedrock = boto3.client(service_name="bedrock-runtime",region_name="us-east-1")

prompt = "<s>[INST] Hola me llamo marco como estas[/INST]"

body = json.dumps({
    "prompt": prompt,
    "max_tokens": 512,
    "top_p": 0.2,
    "temperature": 0.5,
})

modelId = "mistral.mixtral-8x7b-instruct-v0:1"

accept = "application/json"
contentType = "application/json"

response = bedrock.invoke_model(
    body=body,
    modelId=modelId,
    accept=accept,
    contentType=contentType
)

print(json.loads(response.get('body').read()))