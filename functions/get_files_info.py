import os
import os.path as op


def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_dir_abs = op.abspath(working_directory)
    target_dir = op.normpath(op.join(working_dir_abs, directory))

    broken_path = False
    try:
        op.isdir(target_dir)
    except Exception as e:
        broken_path = True

    if broken_path or not op.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    is_valid_target_dir = op.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not is_valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    # else:
    #     return f'Success: "{directory}" is within the working directory'

    dir_info = f"Result for {directory} directory:\n"
    for file in os.listdir(target_dir):
        if file is not None:
            full_path = op.join(target_dir, file)
            dir_info += f"- {file}: file_size={op.getsize(full_path)}, is_dir={op.isdir(full_path)}\n"

    return dir_info

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
            "required": ["directory"]
        },
    },
}
