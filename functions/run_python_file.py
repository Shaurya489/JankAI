import os
import subprocess
def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs=os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        if(not valid_target_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif(not os.path.isfile(target_path)):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif(not target_path.endswith('.py')):
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", target_path]
            if(args):
                command.extend(args)
            result=subprocess.run(command,capture_output=True,text=True,cwd=working_dir_abs,timeout=30)
            if(result.returncode!=0):
                return f'Process exited with code {result.returncode}'
            elif(not result.stderr and not result.stdout):
                return "No output produced"
            elif(result.stderr):
                return f'STDERR: {result.stderr}'
            elif(result.stdout):
                return f'STDOUT: {result.stdout}'
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Gives the ability to run a python file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the python file, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "string list",
                    "description": "List of the arguments to be used for running the python code, It can also be None",
                },
            },
        },
    },
}