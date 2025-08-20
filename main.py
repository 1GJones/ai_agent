import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from functions.get_files_info import  schema_get_files_info,schema_get_file_content,schema_run_python_file,schema_write_file
from call_function import call_function
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

available_functions = genai.types.Tool(function_declarations=[
       schema_get_files_info,
       schema_get_file_content,
       schema_run_python_file,
       schema_write_file
   ]
)
# model Name / load the model
model = genai.GenerativeModel(
   model_name="gemini-1.5-flash",
   system_instruction= system_prompt
)
# Call the model
messages =  [{"role": "user", "parts":[ prompt]}]

response = model.generate_content(contents =messages, tools=[available_functions]
)
# Always print the response
print("Response:")
if response.candidates:
    parts = response.candidates[0].content.parts
    for part in parts:
    
            function_call_result = call_function(part.function_call, verbose=verbose)

            if (
                function_call_result.get("parts")
                and isinstance(function_call_result["parts"][0], dict)
                and "functionResponse" in function_call_result["parts"][0]
                and "response" in function_call_result["parts"][0]["functionResponse"]
                ):
                if verbose:
                    print(f"-> {function_call_result['parts'][0]['functionResponse']['response']}")
                else:
                    raise RuntimeError("No functionResponse.response found in tool result!")
                print(part.text)
else:
    print("No response content available")       
    
if verbose:
   print(f"User prompt: {prompt}")
try:
    print("Response:\n" + response.text)
except Exception:
    print("No plain text response, only tool/function calls.")
    print(f"\nPrompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

# Print verbose message
    print("\nVerbose:", verbose)

