import os
import os.path as op
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = op.abspath(working_directory)
        target_file = op.normpath(op.join(working_dir_abs, file_path))

        is_valid_target_file = op.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not is_valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not op.exists(target_file) or not op.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        command_output = subprocess.run(command, check=False, capture_output=True, text=True, timeout=30)

        result_output = ""
        if command_output.returncode != 0:
            result_output += f"Process exited with code {command_output.returncode}\n"

        if not command_output.stdout and not command_output.stderr:
            result_output += "No output produced\n"
        if command_output.stdout:
            result_output += f"STDOUT: {command_output.stdout}"
        if command_output.stderr:
            result_output += f"STDERR: {command_output.stderr}"

        return result_output
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python script from a file (as if from the command line)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    'items': {
                        "type": "string"
                    },
                    "description": "File path to the Python script",
                },
                "args": {
                    "type": "array",
                    "description": "Optional command-line arguments to run the Python script with"
                }
            },
            "required": ["file_path"]
        },
    },
}
