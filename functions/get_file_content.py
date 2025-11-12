import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Check if target file is within the working directory, error if not
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Check if target file is actually a file, error if not
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # Read the file and return its contents as a string
    with open(abs_file_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)
    return file_content_string