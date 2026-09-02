import os
import config
def get_files_content(working_directory:str,file_path:str)->str:
    try:
        working_dir_abs=os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        if(not valid_target_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif(not os.path.isfile(target_path)):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(target_path, "r") as f:
                content = f.read(config.MAX_CHARS)
                if f.read(1):
                    content += f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'
                return content
            
    except Exception as e:
        return f'Error:{e}'
    
schema_get_files_content = {
    "type": "function",
    "function": {
        "name": "get_files_content",
        "description": "Gets content from the specified file relative to the working directory. It reads at most MAX_CHARS from the file(10000 by default)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to read the file from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}