import os.path as op


def get_files_info(working_directory: str, directory: str = ".") -> str:
    broken_path = False
    try:
        op.isdir(directory)
    except Exception as e:
        broken_path = True

    if broken_path or not op.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    working_dir_abs = op.abspath(working_directory)
    target_dir = op.normpath(op.join(working_dir_abs, directory))
    valid_target_dir = op.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    else:
        return f'Success: "{directory}" is within the working directory'
