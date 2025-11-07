import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


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
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
    print(response.text)
    if sys.argv[-1] == "--verbose":
        print(f"User prompt: {user_prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
