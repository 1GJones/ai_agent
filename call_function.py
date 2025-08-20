from config import MAX_READ_CHARACTERS
import os
from google.generativeai import types
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file

def call_function(function_call_part, verbose=False):
      """
    Dispatch a tool call (FunctionCall) to one of our four functions and wrap the result
    in a types.Content with a types.Part.from_function_response.
    """
      function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

      function_name = function_call_part.name
      args_in = dict(function_call_part.args or {})

    # Required prints
      if verbose:
        print(f"Calling function: {function_name}({args_in})")
      else:
       print(f" - Calling function: {function_name}")

    # Inject working directory (LLM never sets this)
      kwargs = {**args_in, "working_directory": "./calculator"}

    # Helpful default for vague “run tests” prompts
      if function_name == "run_python_file" and "file_path" not in kwargs:
         kwargs["file_path"] = "tests.py"

    # Unknown function → error Content
      if function_name not in function_map:
       return {
            "role": "tool",
            "parts": [
            {
              "functionResponse": {
                  "name": function_name,
                  "response": {"error": f"Unknown function: {function_name}"},  # Or {"error": ...}
            }
          }
          ]
      }
      try:
        result = function_map[function_name](**kwargs)
        response_dict = {
            "role": "tool",
            "parts": [
                {
                    "functionResponse": {
                        "name": function_name,
                        "response": {"result": result},
                    }
                }
            ]
        }
      except Exception as e:
        response_dict = {
            "role": "tool",
            "parts": [
                {
                    "functionResponse": {
                        "name": function_name,
                        "response": {"error": str(e)},
                    }
                }
            ]
        }

      return response_dict