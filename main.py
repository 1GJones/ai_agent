import os
import sys
from dotenv import load_dotenv
from google import  generativeai as genai
from google.genai import types


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

# Optional secons argument for verbose mode
verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
# Authenticate


# Create the model 
model = genai.GenerativeModel(model_name="gemini-2.0-flash-001")
messages = [ {"role": "user", "parts":[prompt]}]
# Generate Response
response = model.generate_content(contents=messages)

# Always print the respose
print("Response:")
print(response.text)

if verbose:
   print(f"User prompt: {prompt}")
   print("Response:\n" + response.text)
   print(f"\nPrompt tokens: {response.usage_metadata.prompt_token_count}")
   print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

# Print verbose message
   print("\nVerbose:", verbose)

