import os
import subprocess
import sys


def run_python_file(working_directory, file_path, args=[]):
    
    # Use the working directory if no subdirectory is specified
        full_path = os.path.abspath(working_directory)
   
        # Ensure the path stays within working_directory
        base_path = os.path.abspath(os.path.join(working_directory, file_path))
    
        # Guardrail: block traversal outside working_directory
        if not base_path.startswith(full_path):
          return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
      
        if not os.path.exists(base_path):
            return f'Error: File "{file_path}" not found.'
      
        if not base_path.endswith(".py"):
            
            return  f'Error: "{file_path}" is not a Python file.'
        
        try:
            completed_process = subprocess.run(
                ["python3", base_path] + args,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                cwd = working_directory,
                timeout = 30,
                text = True
            )
            stdout = completed_process.stdout or ''
            stderr = completed_process.stderr or ''
            
            if not stdout.strip() and not stderr.strip():
                return "No output produced."
            
            output = stdout + stderr
            if completed_process.returncode != 0:
                output += f"\nProcess exited with code {completed_process.returncode}"
                
            return output.strip()
        
        except Exception as e:
            return f"Error: executing Python file: {e}"
            
