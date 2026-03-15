import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import whether_api
# from config import system_promt

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

FREE_MODEL = "openrouter/free"
TOOLS_FNS = {"whether_api":whether_api}

tools =[
    {
        "type":"function",
        "function":{
            "name":"whether_api",
            "description":"Get the current weather for a city",
            "parameters":{
                "type":"object",
                "properties":{
                    "city_name":{
                        "type":"string",
                        "description":"The name of the city"
                    }
                },  
                "required":["city_name"]
            }
        }
    }
]

conversation = []

# conversation.append({"role": "system", "content": system_promt})
# first_call = client.chat.completions.create(
#     model=FREE_MODEL,
#     messages=conversation,
#     tools=tools,
#     temperature=0.3,
# )

# conversation.append(first_call.choices[0].message)
# print("Assistant:", first_call.choices[0].message.content)
# print("Assistant:", first_call.choices[0].message)

while True: 
    question = input("Ask: ")
    
    if question == "exit":
        break

    conversation.append({"role": "user", "content": question})
    
    res = client.chat.completions.create(
        model=FREE_MODEL,
        messages=conversation,
        tools=tools,
        temperature=0.3,
    )

    msg = res.choices[0].message
    conversation.append(msg)

    if msg.tool_calls:
        tool_call = msg.tool_calls[0]
        function = TOOLS_FNS[tool_call.function.name]
        tool_args = tool_call.function.arguments
        tool_result = function(**json.loads(tool_args))
        
        conversation.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_call.function.name,
            "content": str(tool_result)
        })

        res = client.chat.completions.create(
            model=FREE_MODEL,
            messages=conversation,
            tools=tools,
            temperature=0.3,
        )

        final_msg = res.choices[0].message
        conversation.append(final_msg)
        print("Assistant:", final_msg.content)
    else:
        print("Assistant:", msg.content)

    
    



