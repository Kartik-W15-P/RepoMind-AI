from app.rag.generator import create_llm_client, generate_answer


client = create_llm_client()

context = """
File: app.py

import streamlit as st

st.title("RepoMind AI")

st.write("GitHub Repository Intelligence Assistant")
"""

question = "What is the application called?"

answer = generate_answer(
    question=question,
    context=context,
    client=client,
)

print("\nAnswer:")
print(answer)