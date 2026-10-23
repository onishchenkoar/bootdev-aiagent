import os
import os.path as op

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_abs = op.abspath(working_directory)
    target_file = op.normpath(op.join(working_dir_abs, file_path))

    is_valid_target_file = op.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if not is_valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not op.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(target_file, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if f.read(1):
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string
