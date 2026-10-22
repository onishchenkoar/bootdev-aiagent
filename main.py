# %% Initialize
import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("OpenRouter API key is not found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()
user_prompt = args.user_prompt

# %% Prompt LLM
# user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": user_prompt,
        }
    ],
)


# %% Test
if response.usage is None:
    raise RuntimeError("API request failed")

print(f"User prompt:{user_prompt}")
print(f"Prompt tokens: {response.usage.prompt_tokens}")
print(f"Response tokens: {response.usage.completion_tokens}")
print(f"Response:\n{response.choices[0].message.content}")
