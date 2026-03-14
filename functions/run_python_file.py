import os
import subprocess
from typing import Required
from google import genai
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args:
            command.extend(args)
        completed_process = subprocess.run(
            command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30
        )
        if completed_process.returncode != 0:
            return f'Process exited with code "{completed_process.returncode}"'
        if not (completed_process.stderr or completed_process.stdout):
            return "No output produced"
        return f'STDOUT: "{completed_process.stdout}"  \n STDERR: "{completed_process.stderr}"'

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python (.py) script within a specified working directory. "
        "Use this tool when the user asks to 'run', 'execute', 'test', or 'start' a script. "
        "It captures and returns both standard output (STDOUT) and error logs (STDERR)."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the .py file to be executed (e.g., 'script.py' or 'tools/process.py').",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional list of command-line arguments to pass to the script.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        # Added working_directory to required to ensure your function gets the parameter it needs
        required=["file_path"],
    ),
)
