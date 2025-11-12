import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *
from functions.get_files_info import schema_get_files_info
from call_function import available_functions


def main():

    if len(sys.argv) <= 1 or (len(sys.argv) == 2 and sys.argv[1] == "--verbose"):
        print("Error: Please enter a prompt!")
        exit(1)
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL, 
        contents=messages, 
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling functions: {function_call.name}({function_call.args})")
    else:
        print(response.text)
    if sys.argv[-1] == "--verbose":
        print(f"User prompt: {user_prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
