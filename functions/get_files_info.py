import os
from config import MAX_READ_CHARACTERS
from google.generativeai import types

from functions.run_python import run_python_file 
  
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
    
def get_file_content(working_directory, file_path):
    try:  
        full_path = os.path.abspath(os.path.join(working_directory, file_path ))
        base_path = os.path.abspath(working_directory)
        
        if not full_path.startswith(base_path):
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

        
        if not os.path.exists(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        if not os.path.isfile(full_path):
            return f'Error: File "{file_path}" does not a exist'
    
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_READ_CHARACTERS)
        
        if len(content) > MAX_READ_CHARACTERS:
            return content[:MAX_READ_CHARACTERS] + f'\n\n[...File "{file_path}" truncated at {MAX_READ_CHARACTERS} characters]' 
        return content

    except Exception as e:
        return f"Error: {str(e)}"    
        
def write_file(working_directory, file_path, content):
    try:
        abs_working_path = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))
        
        # Check if file is within working_directory
        if not abs_file_path.startswith(abs_working_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'



        # Ensure parent directories exist
        os.makedirs(os.path.dirname(abs_file_path), exist_ok= True)
        
        # Write to file
        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)
            f.truncate
            
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"   
    
def call_function(function_call_part, verbose=False):
    function_map = {
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
    "get_files_info": get_files_info
}
    function_name = function_call_part.name
    args = dict(function_call_part.args)

    
    # 🧪 Log what the LLM gave us
    if verbose:
        print(f"🔍 Function to call: {function_name}")
        print(f"🧾 Raw args received: {args}")

    # Add required working_directory
    args["working_directory"] = "./calculator"
    
    
    # 🛠️ Handle vague "run test suite" style prompts
    if function_name == "run_python_file":
        # If no file_path was provided, default to "tests.py"
        if "file_path" not in args:
            if any(keyword in args.get("task", "").lower() for keyword in ["test", "suite"]):
                args["file_path"] = "tests.py"
            else:
                # Use fallback anyway — optional
                args["file_path"] = "tests.py"

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
        
    
    
    # Call the actual function with unpacked keyword arguments
    try:
        function_result = function_map[function_name](**args)
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": str(e)},
                )
            ],
        )

    # Wrap the result into a valid response format
    result_content = types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

    # If verbose, print the function result
    if verbose:
        print(f"-> {result_content.parts[0].function_response.response}")

    return result_content
     
    
    
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
