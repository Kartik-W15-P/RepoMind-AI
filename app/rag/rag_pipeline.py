from app.rag.embeddings import (
    load_embedding_model,
    generate_embedding,
)

from app.rag.vector_store import (
    create_vector_store,
    search_documents,
)

from app.rag.generator import (
    create_llm_client,
    generate_answer,
)


def retrieve_context(
    question: str,
    collection,
    embedding_model,
    top_k: int = 3,
) -> tuple[str, list[dict]]:
    """Retrieve relevant repository chunks for a question."""

    query_embedding = generate_embedding(
        question,
        embedding_model,
    )

    document_count = collection.count()

    if document_count == 0:
        return "", []

    top_k = min(top_k, document_count)

    results = search_documents(
        collection,
        query_embedding,
        top_k=top_k,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return "", []

    context_parts = []

    for index, (document, metadata) in enumerate(
        zip(documents, metadatas),
        start=1,
    ):
        source = metadata.get(
            "source",
            "Unknown file",
        )

        file_type = metadata.get(
            "file_type",
            "unknown",
        )

        chunk_index = metadata.get(
            "chunk_index",
            0,
        )

        context_parts.append(
            f"[Source {index}]\n"
            f"File: {source}\n"
            f"Type: {file_type}\n"
            f"Chunk: {chunk_index}\n"
            f"Content:\n"
            f"{document}"
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

    # Make sure a repository has been indexed.
    if collection.count() == 0:
        return (
            "No repository has been indexed yet. "
            "Please index a GitHub repository first.",
            [],
        )

    embedding_model = load_embedding_model()

    context, sources = retrieve_context(
        question=question,
        collection=collection,
        embedding_model=embedding_model,
        top_k=top_k,
    )

    if not context:
        return (
            "I couldn't find enough information "
            "in the repository context.",
            [],
        )

    llm_client = create_llm_client()

    answer = generate_answer(
        question=question,
        context=context,
        client=llm_client,
    )

    # Do not display sources when the answer is unsupported.
    unsupported_message = (
        "I couldn't find enough information "
        "in the repository context."
    )

    if unsupported_message in answer:
        return answer, []

    return answer, sources