import os
import config
def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs=os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        if(not valid_target_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif(os.path.isdir(target_path)):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        else:
            os.makedirs(os.path.dirname(target_path),exist_ok=True)
            with open(target_path, "w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            
    except Exception as e:
        return f'Error:{e}'