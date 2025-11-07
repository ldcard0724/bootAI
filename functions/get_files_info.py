import os

def get_files_info(working_directory, directory="."):
    # join working directory and directory together safely
    full_path = os.path.join(working_directory, directory)

    # check if full_path is inside the working directory, immediately stop if not
    try:
        abs_working_path = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)
        if not abs_full_path.startswith(abs_working_path):
            return "f'Error: Cannot list \"{directory}\" as it is outside the permitted working directory'"
    except Exception:
        return "Error!"
    
    # check to ensure directory variable is actually a directory, error if not
    try:
        if not os.path.isdir(directory):
            return "f'Error: \"{directory}\" is not a directory'"
    except Exception:
        return "Error 2!"
    
    # build output string
    output_string = []
    for file in os.listdir(abs_full_path):
        output_string.append(f"- {file}: file_size={os.path.getsize(os.path.join(abs_full_path, file))}, is_dir={os.path.isdir(os.path.join(abs_full_path, file))}")
    
    return "\n".join(output_string)