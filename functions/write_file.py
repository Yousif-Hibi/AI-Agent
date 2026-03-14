import os
from google import genai
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(file_path):
            return f'Error: Cannot write to "{target_file}" as it is a directory'
        target_dir = os.path.dirname(target_file)
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)
        with open(target_file, "w") as file:
            file.write(content)

        return (
            f'Successfully wrote to "{
                file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error listing files: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="takes a file and content and writes the content on the file and return that the data was wrtine correctly ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to write to in the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
