import os
def get_files_info(working_directory:str,directory:str=".")->str:
    try:
        working_dir_abs=os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if(valid_target_dir==False):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        else:
            return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f'Error:{e}'