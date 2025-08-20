import os
from config import MAX_READ_CHARACTERS
from google.generativeai import types
 
  

def get_files_info(working_directory, directory=None):
    try:
        # Use the working directory if no subdirectory is specified
        full_path = os.path.abspath(os.path.join(working_directory,directory or ""))
   
        # Ensure the path stays within working_directory
        base_path = os.path.abspath(working_directory)
    
        # Guardrail: block traversal outside working_directory
        if not full_path.startswith(base_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    
        if not os.path.exists(full_path):
            return f'Error: Path "{directory }" does not exist'
    
        if not os.path.isdir(full_path):
            return f'Error: "{directory }" is not a directory'
    
        # Collect file info
        # Scan directory contents
        output = []
        with os.scandir(full_path) as entries:
            for entry in entries:
                try:
                    size = entry.stat().st_size
                    output.append(f"{entry.name}: file_size ={size} bytes, is_dir={entry.is_dir()} ")
                except Exception as e :
                    output.append(f"{entry.name}: Error: {str(e)}")
        
        return "\n".join(output) if output else "No files found."
    except Exception as e:
        return f"Error: {str(e)}"
    
        
        
schema_get_files_info = types.FunctionDeclaration(
    name ="get_files_info",
    description= "Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters={
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            },
        },
    }

)
schema_get_file_content = types.FunctionDeclaration(
    name ="get_file_content",
    description= "Reads and returns the content of a single file specified by its path.",
    parameters={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The full relative or absolute path to the file whose contents should be read (e.g., 'src/main.py'). This field is required.",
            
            },
        },
        "required": ['file_path']
    }

)
schema_run_python_file = types.FunctionDeclaration(
    name ="run_python_file",
    description= "Executes a single Python script located at the specified file path.",
    parameters={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The full relative or absolute path to the Python file to execute (e.g., 'scripts/example.py'). This field is required.",
            },
            "args": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "Optional list of command-line arguments to pass to the Python script (e.g., ['--mode', 'test', '--count', '5'])."
            },
        },
            
        "required": ['file_path']
    }

)
schema_write_file = types.FunctionDeclaration(
    name ="write_file",
    description="Creates or overwrites a file at the specified path with the provided content.",
    parameters={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The full relative or absolute path where the file should be written (e.g., 'output/result.txt').",
            },
            "content": {
                "type": "string",
                "description": "The full text content to write into the file.",
            },
        },
        "required": ["file_path", "content"]
    }
)
