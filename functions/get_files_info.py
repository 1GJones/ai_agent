import os
from config import MAX_READ_CHARACTERS
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
        full_path = os.path.abspath(os.path.join(working_directory,os.path.basename(file_path )))
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
        