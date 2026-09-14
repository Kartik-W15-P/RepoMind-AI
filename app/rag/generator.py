import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"


def create_llm_client() -> InferenceClient:
    """Create a Hugging Face inference client."""
    load_dotenv()

    token = os.getenv("HF_TOKEN")

    if not token:
        raise ValueError("HF_TOKEN was not found.")

    return InferenceClient(
        token=token,
        provider="nscale",
    )


def generate_answer(
    question: str,
    context: str,
    client: InferenceClient,
) -> str:
    """Generate a grounded answer using the retrieved repository context."""

    prompt = f"""
You are RepoMind AI, a GitHub repository intelligence assistant.

Answer the user's question using ONLY the repository context provided below.

If the answer cannot be found in the provided context, say:
"I couldn't find enough information in the repository context."

Do not invent files, functions, technologies, or behavior.

Repository context:
-------------------
{context}
-------------------

User question:
{question}

Give a clear and concise answer.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=500,
    )

    return response.choices[0].message.content