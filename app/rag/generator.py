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

Your task is to answer the user's question using ONLY the repository
context provided below.

STRICT RULES:

1. Use only information explicitly present in the repository context.
2. Do not invent files, functions, classes, APIs, technologies, or behavior.
3. If the context does not contain enough information to answer the question,
   respond exactly with:
   "I couldn't find enough information in the repository context."
4. When describing implementation details, mention the relevant file path
   whenever it is available in the context.
5. If multiple files contribute to the answer, explain their roles separately.
6. Do not assume that a common software pattern exists unless the repository
   context explicitly shows it.
7. Keep the answer clear, concise, and technically accurate.

REPOSITORY CONTEXT
==================
{context}
==================

USER QUESTION
=============
{question}
=============

Now answer the question using only the repository context.
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