import os
import sys
import json

# Add the parent directory (ai-agent-01) to sys.path so we can import tools and config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai import OpenAI
from dotenv import load_dotenv
from tools import tools
from config import react_system_prompt, planner_prompt

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
MAX_ITERATION = 10
models= "openrouter/free"


chat_history = []
summary = ""


tools_desc = []
for t in tools:
    for name, details in t.items():
        clean_details = {k: v for k, v in details.items() if k != 'fn'}
        tools_desc.append(f"Tool Name: {name}\nDetails: {json.dumps(clean_details, indent=2)}")
tools_desc = '\n\n'.join(tools_desc)

system = react_system_prompt.format(tool_descriptions=tools_desc)
planner_system = planner_prompt.format(tool_names=tools_desc)

"""
 --- ALL CHATS -----

1. System prompt - 
2. chat history - 
3. summary - 
"""

"""
 --- SINGLE CHAT ----

 whenever not getfinal output it iterate in this formate (R A O)

1. Resoning  - LLM will think about the problem and provide output ()
2. Action  - Based on LLM output select and call tool
3. observation - Result of tool call

"""



while True:
    user_input = input("User: ")
    if user_input == "exit":
        break
    
    chat_history.append({"role":"system","content":system})
    chat_history.append({"role": "user", "content": user_input})
    message = []
    message.append({"role":"system","content":system})
    # message.append({"role": "user", "content": user_input})

    plan_steps_response = client.chat.completions.create(
        model=models,
        messages=[
            {"role":"system","content":planner_system},
            {"role":"user","content":user_input},
            {"role":"user","content": json.dumps(chat_history)}
        ]
    )
    plan_steps_str = plan_steps_response.choices[0].message.content

    try:
        plan_steps_dict = json.loads(plan_steps_str)
        print('execution plan :: ', plan_steps_dict.get('steps', []))
    except json.JSONDecodeError:
        print('execution plan parsing failed. Raw output:', plan_steps_str)
        plan_steps_dict = {"steps": [], "raw": plan_steps_str}

    # IMPORTANT: The message content MUST be a string, not a dictionary.
    # We combine the user's input with the plan so the ReAct agent has all context.
    prompt_content = f"User Request: {user_input}\n\nExecution Plan:\n{json.dumps(plan_steps_dict)}"
    message.append({"role":"user","content": prompt_content})
    
    


    for i in range(MAX_ITERATION):
        
        response = client.chat.completions.create(
            model=models,
            messages=message,
            temperature=0.3,
        )
        
        response_message = response.choices[0].message
        print('response message',response_message)
        print("Assistant: ",response_message.content)

        content = response_message.content

        message.append({"role": "assistant", "content": content})

        try:
            parsed_response = json.loads(response_message.content)
        except json.JSONDecodeError:
            print("Failed to parse response as JSON. Exiting loop.")
            break

        
        if "final_answer" in parsed_response:
            print("Final Answer:", parsed_response['final_answer'])
            chat_history.append({"role": "assistant", "content": parsed_response['final_answer']})
            break
            
        if "action" in parsed_response:
            print("========Tool Calls:========")
            tool_name = parsed_response["action"]
            tool_args = parsed_response.get("action_input", {})
            

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



        
        
