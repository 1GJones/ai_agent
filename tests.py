import os
from functions.get_files_info import  write_file
from functions.run_python import run_python_file

# Define working directory(the root of your project)
working_dir = os.path.abspath(os.path.dirname(__file__))

     
if __name__ == "__main__":
    

    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))    
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print(run_python_file("calculator",'Error: File "nonexistent.py" not found.'))
    print(run_python_file("calculator", 'Error: Cannot execute "../main.py" as it is outside'))