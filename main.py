import os
import sys

from dotenv import load_dotenv
from google import generativeai as genai
from google.generativeai import types
from google.ai.generativelanguage import Content, Part
from functions.get_files_info import  get_file_content, get_files_info, schema_get_files_info,schema_get_file_content,schema_run_python_file,schema_write_file, write_file
from functions.run_python import run_python_file

# Load environment variables
load_dotenv()

# Force-set the correct environment variable name
os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

# Get the API key
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
   raise ValueError("❌ Missing GOOGLE_API_KEY in environment. Check your .env file.")
# Configure Gemini key
genai.configure(api_key=api_key)

# Get the prompt from command-line arguments
if len(sys.argv) < 2:
   raise ValueError("❌ Please provide BOTH a prompt and a verbose message.\n\nUsage:\n  python3 main.py \"<prompt>\" \"<verbose>\"")

# First argument is the prompt
prompt = (sys.argv[1])


# Optional seconds argument for verbose mode
verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
# Authenticate

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Prompt message 

def call_function(function_call_part, verbose=False):
    function_map = {
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
        "get_files_info": get_files_info,
    }

    function_name = function_call_part.name

    # Handle unknown function: return an error Content
    if function_name not in function_map:
        return Content(
            role="tool",
            parts=[
                Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Copy/inject args
    args = dict(function_call_part.args or {})
    args["working_directory"] = "./calculator"

    # Default tests filename for vague prompts
    if function_name == "run_python_file" and "file_path" not in args:
        args["file_path"] = "tests.py"

    # Execute and wrap result in a Content object
    try:
        fn = function_map[function_name]
        function_result = fn(**args)
        part = Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    except Exception as e:
        part = Part.from_function_response(
            name=function_name,
            response={"error": str(e)},
        )

    content = Content(role="tool", parts=[part])

    if verbose and hasattr(part, "function_response") and hasattr(part.function_response, "response"):
        print(f"-> {part.function_response.response}")

    return content   
if verbose:
   print(f"User prompt: {prompt}")
# Print verbose message
   print("\nVerbose:", verbose)

