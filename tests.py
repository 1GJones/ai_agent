import os
from functions.get_files_info import get_files_info

# Define working directory(the root of your project)
working_dir = os.path.abspath(os.path.dirname(__file__))

def run_test(name, directory=None):
    print(f"\nRunning. test: {name}")
    result = get_files_info(working_dir,directory)
    print(result)
    print("Result for current directory:")
    print(get_files_info("calculator", "."))

    print("\nResult for 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))
    
if __name__ == "__main__":
    # ✅ Test 1: No directory provided (should list root contents)
    run_test("Root directory")

    # ✅ Test 2: Valid subdirectory
    run_test("Valid subdirectory: 'calculator'", "calculator")

    # ✅ Test 3: Invalid subdirectory path (should return out-of-bounds error)
    run_test("Out-of-bounds directory", "../")

    # ✅ Test 4: File instead of directory (should return 'not a directory')
    run_test("Not a directory", "README.md")

    # ✅ Test 5: Non-existent directory
    run_test("Non-existent directory", "does_not_exist")
