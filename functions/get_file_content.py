import os
from config import MAX_READ_CHARACTERS
from google.generativeai import types
 

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
