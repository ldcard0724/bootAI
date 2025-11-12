import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *
from functions.get_files_info import schema_get_files_info
from call_function import *


def main():
    load_dotenv()

    # Check arguments, set verbose flag if --verbose was passed in from the command line
    verbose = "--verbose" in sys.argv

    # Add args from command line that aren't prefixed with '--' to args list
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    for i in range(0, 20):
        try:
            gen_content_response = generate_content(client, messages, verbose)
            if gen_content_response:
                print(gen_content_response)
                break
        except Exception as e:
            print(e)


def generate_content(client, messages, verbose):
    response=client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
        

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    if not response.function_calls:
        return response.text

    function_responses=[]
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)

        if not function_call_result.parts or not function_call_result.parts[0].function_response:
            raise Exception("empty function call result")
        
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
        messages.append(types.Content(
            role="user",
            parts=[function_call_result.parts[0]]
        ))
    
    if not function_responses:
        raise Exception("no function responses generated, exiting.")

if __name__ == "__main__":
    main()
