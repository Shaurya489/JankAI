import os
def get_files_info(working_directory:str,directory:str=".")->str:
    try:
        working_dir_abs=os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if(valid_target_dir==False):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            return f'Error: "{directory}" is not a directory'
        else:
            files_data=[]
            with os.scandir(target_dir) as entries:
                for entry in entries:
                    attributes=entry.stat()
                    file_info={
                        "name":entry.name,
                        "file_size":attributes.st_size,
                        "is_dir":entry.is_dir(),
                    }
                    files_data.append(file_info)
            return files_data
    except Exception as e:
        return f'Error:{e}'
    
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}