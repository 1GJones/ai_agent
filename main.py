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

# Get the prompt from command-line arguments
if len(sys.argv) < 2:
   raise ValueError("❌ Please provide a prompt as a command-line argument.")
prompt = " ".join(sys.argv[1:])

# Authenticate

# Configure Gemini key
genai.configure(api_key=api_key)

# Create the model 
model = genai.GenerativeModel(model_name="gemini-2.0-flash-001")
messages = [ {"role": "user", "parts":[prompt]}]
# Generate Response
response = model.generate_content(
   contents=messages
)
print(response.text)
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


