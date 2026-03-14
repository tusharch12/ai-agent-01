import os
from dotenv import load_dotenv
from openai import OpenAI
import requests

load_dotenv()

FREE_MODEL = "openrouter/free"
TOOL_MODEL = "openrouter/free"

conversation =[{'role':'user','content':'What is fundamental of economics? answer in one line'}]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

response1 = client.chat.completions.create(
    model=FREE_MODEL,
    messages=conversation,
    temperature=0.0,
    # max_tokens=50,
)
turn1=response1.choices[0].message.content

print(f"Response: {response1.choices[0].message.content}")
print(f"tokens: {response1.usage.total_tokens}")
print(f"Model: {response1.model}")

conversation.append({'role':'assistant','content':turn1})
conversation.append({'role':'user','content':'Give an example that justify fundatementals of economics? answer in one line'})

response2 = client.chat.completions.create(
    model=FREE_MODEL,
    messages=conversation,
    temperature=0.0,
    # max_tokens=50,
)
turn2=response2.choices[0].message.content

conversation.append({'role':'assistant','content':turn2})

print(f"Response: {response2.choices[0].message.content}")
print(f"tokens: {response2.usage.total_tokens}")
print(f"Model: {response2.model}")



