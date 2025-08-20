import os
from config import MAX_READ_CHARACTERS
import google.generativeai as types

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
    
