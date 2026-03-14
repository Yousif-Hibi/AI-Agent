import os
from config import MAX_CHAR_LIMIT
from google import genai
from google.genai import types


def get_file_content(working_directory, file_path):

    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        file = open(target_file)
        file_content = file.read(MAX_CHAR_LIMIT)
        if file.read(1):
            file_content += (
                f'[...File "{file_path}" truncated at {
                    MAX_CHAR_LIMIT} characters]'
            )
        return file_content

    except Exception as e:
        return f"Error listing files: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"],
    ),
)
