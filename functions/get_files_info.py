import os
def get_files_info(working_directory, directory=None):
    try:
   # Use the working directory if no subdirectory is specified
        __path__ = os.path.abspath(os.path.join(working_directory,directory or ""))
   
     # Ensure the path stays within working_directory
        working_directory = os.path.abspath(working_directory)
    
    # Guardrail: block traversal outside working_directory
        if not __path__.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    
        if not os.path.exists(__path__):
            return f'Error: Path "{directory or "."}" does not exist'
    
        if not os.path.isdir(__path__):
            return f'Error: "{directory or "."}" is not a directory'
    
    # Collect file info
    # Scan directory contents
        output = []
        with os.scandir(__path__) as entries:
            for entry in entries:
                try:
                    size = entry.stat().st_size
                    output.append(f"📄 {entry.name}: file_size ={size} bytes, is_dir={entry.is_dir()} ")
                except Exception as e :
                    output.append(f"📁 {entry.name}: Error: {str(e)}")
        
        return "\n".join(output) if output else "No files found."
    except Exception as e:
        return f"Error: {str(e)}"