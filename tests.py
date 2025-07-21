import os
from functions.get_files_info import get_files_info, write_file

# Define working directory(the root of your project)
working_dir = os.path.abspath(os.path.dirname(__file__))

     
if __name__ == "__main__":
    

    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))    
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    