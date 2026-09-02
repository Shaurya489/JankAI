from functions.get_files_info import schema_get_files_info 
from functions.get_files_content import schema_get_files_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

available_functions = [
    schema_get_files_info,
    schema_get_files_content,
    schema_run_python_file,
    schema_write_file
]