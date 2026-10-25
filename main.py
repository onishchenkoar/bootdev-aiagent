import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


def init_llm_client():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("OpenRouter API key is not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    return client

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if args.verbose:
        print(f"User prompt:{args.user_prompt}")

    client = init_llm_client()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    call_llm(client, messages, verbose=True)

def call_llm(client: OpenAI, messages: list[str], verbose: bool):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
    )

    if response.usage is None:
        raise RuntimeError("API request failed")

    message = response.choices[0].message
    if message.tool_calls:
        for tool_call in message.tool_calls:
            # function_args = json.loads(tool_call.function.arguments or "{}")
            # print(f"Calling function: {tool_call.function.name}({function_args})")
            result_message = call_function(tool_call, verbose)
            if not result_message["content"]:
                raise Exception("Something wrong: the response content is empty")
            if verbose:
                print(f"-> {result_message['content']}")

    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

if __name__ == "__main__":
    main()