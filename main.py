import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


MAX_LLM_STEPS = 20

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

    tool_calls = False
    for _ in range(MAX_LLM_STEPS):
        tool_calls, llm_response_messages = call_llm(client, messages, verbose=args.verbose)
        messages.extend(llm_response_messages)
        if not tool_calls:
            break

    if tool_calls:
        print(f"LLM did not manage to do its job in {MAX_LLM_STEPS} iterations.")
        sys.exit(1)


def call_llm(client: OpenAI, messages: list[str], verbose: bool):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
    )

    if response.usage is None:
        raise RuntimeError("API request failed")

    llm_response_message = response.choices[0].message
    response_messages = [llm_response_message]
    if llm_response_message.tool_calls:
        tool_calls = True
        for tool_call in llm_response_message.tool_calls:
            tool_response_message = call_function(tool_call, verbose)
            if not tool_response_message["content"]:
                raise Exception("Something wrong: the response content is empty")
            response_messages.append(tool_response_message)
            if verbose:
                print(f"-> {tool_response_message['content']}")
    else:
        tool_calls = False
        print(f"Final response: {llm_response_message.content}")

    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    return (tool_calls, response_messages)

if __name__ == "__main__":
    main()
