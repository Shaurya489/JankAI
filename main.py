import os
import json
from pathlib import Path
import getpass
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions,call_function

def get_api_key():
    api_key=os.environ.get("OPENROUTER_API_KEY")
    if api_key:
        return api_key
    
    config_path = Path.home() / ".jankai_key"
    if config_path.exists():
        key = config_path.read_text().strip()
        if key:
            return key
        
    print("\n[JankAI Setup] OpenRouter API key not found.")
    print("Get a free key at: https://openrouter.ai/keys\n")
    
    api_key = getpass.getpass("Enter your OpenRouter API key: ").strip()
    
    if not api_key:
        raise RuntimeError("Error: An OpenRouter API key is required to use JankAI.")

    config_path.write_text(api_key)
    print(f"API key saved successfully to {config_path}\n")
    
    return api_key

def cli_entry():
    load_dotenv()
    api_key = get_api_key()

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

    dynamic_system_prompt=system_prompt+f"Your current working directory is {target_dir}"

    messages=[
        {"role": "system", "content": dynamic_system_prompt},
        {"role":"user","content":args.user_prompt}
    ]

    for _ in range(20):
        response=client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions
        )

        if response is None or response.choices is None or len(response.choices) == 0:
            print("Error: OpenRouter returned an empty response or hit a rate limit.")
            break

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
        
if __name__=="__main__":
    cli_entry()