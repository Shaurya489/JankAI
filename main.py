import os
import json
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions,call_function

load_dotenv()
api_key=os.environ.get("OPENROUTER_API_KEY")

if(api_key==None):
    raise RuntimeError("API Key not found")

from openai import OpenAI
import argparse

parser=argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt",type=str,help="User prompt")
parser.add_argument("--dir",type=str,default=".",help="Target working directory")
parser.add_argument("--verbose",action="store_true",help="Enable Verbose Output")
args=parser.parse_args()

target_dir=os.path.abspath(args.dir)

client=OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

system_prompt=system_prompt+f"Your current working directory is {target_dir}"

messages=[
    {"role": "system", "content": system_prompt},
    {"role":"user","content":args.user_prompt}
]

for _ in range(20):
    response=client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
    )


    message = response.choices[0].message
    messages.append(message)
    
    if not message.tool_calls:
        print("Response:")
        print(message.content)
        break
    
    for tool_call in message.tool_calls:
        result_message=call_function(tool_call,args.verbose,target_dir)
        if not result_message["content"]:
            raise Exception("Function call returned empty content")

        if args.verbose:
            print(f"-> {result_message['content']}")
        
        messages.append(result_message)
else:
    print("Maximum iterations reached")