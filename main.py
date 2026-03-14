import os
import call_function
import config
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt, model_name
from call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeErro("API Key didn't load")
    client = genai.Client(api_key=api_key)
    function_reponses = []
    messages = [types.Content(
        role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        candidates = response.candidates
        for candidate in candidates:
            messages.append(candidate.content)
        if not call_api(response, args):
            return
        function_reponses.append(call_api(response, args))
        messages.append(function_reponses[-1])
    exit(1)


def call_api(response, args):
    function_reponses = []
    if response.function_calls:
        for call in response.function_calls:
            call_result = call_function(call)
            if not call_result.parts:
                raise Exception("Error: Parts is None")

            if not call_result.parts[0].function_response:
                raise Exception("Error: the funtion response is None")

            if not call_result.parts[0].function_response.response:
                raise Exception("Erorr: the final response is none")

            function_reponses.append(call_result.parts[0])
            if args.verbose:
                print(f"-> {call_result.parts[0].function_response.response}")

    else:
        print(response.text)
        return None
    if args.verbose:
        print(f"-> {function_reponses[0].function_response.response}")
    return function_reponses


if __name__ == "__main__":
    main()
