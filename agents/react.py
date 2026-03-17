import os
import json
import openai
from openai import OpenAI
from dotenv import load_dotenv
from tools import whether_api
from config import react_system_prompt
from tools import tools

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

FREE_MODEL = "openrouter/free"

tools_desc = []
for t in tools:
    for name, details in t.items():
        clean_details = {k: v for k, v in details.items() if k != 'fn'}
        tools_desc.append(f"Tool Name: {name}\nDetails: {json.dumps(clean_details, indent=2)}")
tools_desc = '\n\n'.join(tools_desc)

print('tools_desc',tools_desc)
system = react_system_prompt.format(tool_descriptions=tools_desc)
max_iteration = 15

message = [
    {'role':'system','content':system},
]



while True: 
    user_input = input("User: ")
    if user_input == "exit":
        break
    message.append({'role':'user','content':user_input})
    
    for i in range(max_iteration):

        print('========Iteration:========',i)

        try:
            response = client.chat.completions.create(
                model=FREE_MODEL,
                messages=message,
                temperature=0.3,
            ) 
        except openai.RateLimitError as e:
            print("\n[!] The free AI model is currently rate-limited. Please wait a moment and try again.\n")
            break

        response_message = response.choices[0].message
        print(f"Assistant: {response_message.content}")

        # Parse the JSON string from the response
        try:
            parsed_response = json.loads(response_message.content)
        except json.JSONDecodeError:
            print("Failed to parse response as JSON. Exiting loop.")
            break

        # Check if the assistant has the final answer
        if "final_answer" in parsed_response:
            print("Final Answer:", parsed_response['final_answer'])
            break
            
        # Check if the assistant wants to call a tool
        if "action" in parsed_response:
            print("========Tool Calls:========")
            tool_name = parsed_response["action"]
            tool_args = parsed_response.get("action_input", {})
            
            # Find the correct function in the tools list
            function_to_call = None
            for t in tools:
                if tool_name in t:
                    function_to_call = t[tool_name]['fn']
                    break
            
            if function_to_call:
                obersevation = function_to_call(**tool_args)
                message.append({
                    'role':'user',
                    'content':str(obersevation)
                })
                print("Observation:", obersevation)
            else:
                print(f"Tool {tool_name} not found.")
                break