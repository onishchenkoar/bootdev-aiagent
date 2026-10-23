import os
import os.path as op


def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs = op.abspath(working_directory)
    target_file = op.normpath(op.join(working_dir_abs, file_path))

    is_valid_target_file = op.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if not is_valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if op.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    os.makedirs(op.dirname(target_file), exist_ok=True)
    with open(target_file, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
