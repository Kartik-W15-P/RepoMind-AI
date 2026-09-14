import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

token = os.getenv("HF_TOKEN")

if not token:
    raise ValueError("HF_TOKEN was not found.")

client = InferenceClient(
    token=token,
    provider="nscale",
)

response = client.chat.completions.create(
    model="Qwen/Qwen3-4B-Instruct-2507",
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: RepoMind connection works."
        }
    ],
    max_tokens=30,
)

print(response.choices[0].message.content)