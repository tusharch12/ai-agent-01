import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

FREE_MODEL = "openrouter/free"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

conversation = []
summary = ""
WINDOW = 6


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
        temperature=0.0,
    )

    return res.choices[0].message.content


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
