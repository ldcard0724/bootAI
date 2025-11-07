import os
from config import MAX_CHARS

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))
    # Check if target directory is within the working directory, error if not
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as is is outside the permitted working directory'
    # Check if target is actually a directory, error if not
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        output_string = []
        for file in os.listdir(target_dir):
            filepath = os.path.join(target_dir, file)
            output_string.append(f"- {file}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}")
        return "\n".join(output_string)
    except Exception as e:
        return f"Error listing files: {e}"
    
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