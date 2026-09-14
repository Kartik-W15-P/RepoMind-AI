from pathlib import Path

from app.rag.embeddings import load_embedding_model, generate_embedding
from app.rag.vector_store import create_vector_store, search_documents
from app.rag.generator import create_llm_client, generate_answer


def retrieve_context(
    question: str,
    collection,
    embedding_model,
    top_k: int = 3,
) -> tuple[str, list[dict]]:
    """Retrieve the most relevant repository chunks for a question."""

    query_embedding = generate_embedding(
        question,
        embedding_model,
    )

    results = search_documents(
        collection,
        query_embedding,
        top_k=top_k,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for document, metadata in zip(documents, metadatas):
        source = metadata.get("source", "Unknown file")

        context_parts.append(
            f"File: {source}\n"
            f"Content:\n{document}"
        )

    context = "\n\n---\n\n".join(context_parts)

    return context, metadatas


def ask_repository(
    question: str,
    vector_store_path: str = "chroma_db",
    top_k: int = 3,
) -> tuple[str, list[dict]]:
    """Answer a question using repository retrieval and the LLM."""

    collection = create_vector_store(
        persist_directory=vector_store_path
    )

    embedding_model = load_embedding_model()

    context, sources = retrieve_context(
        question=question,
        collection=collection,
        embedding_model=embedding_model,
        top_k=top_k,
    )

    llm_client = create_llm_client()

    answer = generate_answer(
        question=question,
        context=context,
        client=llm_client,
    )

    return answer, sources