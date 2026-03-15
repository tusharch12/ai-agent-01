import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import whether_api
from config import system_promt

load_dotenv()

FREE_MODEL = "openrouter/free"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

tools =[
    {
        "type":"function",
        "function":{
            "name":"wheter_api",
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
summary = ""
WINDOW = 6


conversation.append({"role": "system", "content": system_promt})


def summarize(old_summary, old_messages):

    prompt = f"""
You are maintaining long-term memory for a conversation.

Existing summary:
{old_summary}

New messages:
{old_messages}

Update the summary while preserving important facts,
goals, technical topics, and decisions.

Return only the updated summary.
"""

    res = client.chat.completions.create(
        model=FREE_MODEL,
        messages=[
            {"role": "system", "content": prompt}
        ],
        tools=tools,
        temperature=0.0,
    )

    return res.choices[0].message.content


first_run = client.chat.completions.create(
    model=FREE_MODEL,
    messages=conversation,
    tools=tools,
    temperature=0.3,
)

print('Assistant:', first_run.choices[0].message.content)

conversation.append({"role": "assistant", "content": first_run.choices[0].message.content})
    

while True:

    question = input("Ask: ")

    if question == "exit":
        break

    conversation.append({"role": "user", "content": question})

    if len(conversation) > WINDOW:

        old_messages = conversation[:-WINDOW]

        summary = summarize(summary, old_messages)

        conversation = conversation[-WINDOW:]

    messages = []

    messages.append({
        "role": "system",
        "content": f"You are a helpful assistant.\nConversation summary:\n{summary}"
    })

    messages.extend(conversation)

    res = client.chat.completions.create(
        model=FREE_MODEL,
        messages=messages,
        temperature=0.0,
    )

    answer = res.choices[0].message.content

    print("Assistant:", answer)

    conversation.append({"role": "assistant", "content": answer})
