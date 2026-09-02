import os
import json
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions

load_dotenv()
api_key=os.environ.get("OPENROUTER_API_KEY")

if(api_key==None):
    raise RuntimeError("API Key not found")

from openai import OpenAI
import argparse

parser=argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt",type=str,help="User prompt")
parser.add_argument("--verbose",action="store_true",help="Enable Verbose Output")
args=parser.parse_args()

client=OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

messages=[
    {"role": "system", "content": system_prompt},
    {"role":"user","content":args.user_prompt}
]

response=client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions
)

if(args.verbose):
    print(f"User prompt: {messages[0]['content']}")
    if(response.usage==None):
        raise RuntimeError("Request Failed")
    else:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

message = response.choices[0].message

for tool_call in message.tool_calls:
    function_args=json.loads(tool_call.function.arguments or "{}")
    print(f"Calling function : {tool_call.function.name}({function_args})")

print("Response:")
print(message.content)