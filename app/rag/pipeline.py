from pathlib import Path

from app.ingestion.file_filter import filter_repository_files
from app.ingestion.file_reader import read_repository_files
from app.ingestion.chunker import chunk_documents
from app.ingestion.github_loader import get_repository_files

from app.rag.embeddings import (
    load_embedding_model,
    generate_embeddings,
)
from app.rag.vector_store import (
    create_vector_store,
    add_documents,
)


def index_repository(
    repository_path: Path,
) -> dict:
    """Index a repository into ChromaDB."""

    # 1. Get all repository files
    all_files = get_repository_files(repository_path)

    # 2. Keep only relevant files
    selected_files = filter_repository_files(
        all_files,
        repository_path,
    )

    # 3. Read selected files
    documents = read_repository_files(
        selected_files,
        repository_path,
    )

    # 4. Split documents into chunks
    chunks = chunk_documents(documents)

    if not chunks:
        raise ValueError(
            "No readable content found in the repository."
        )

    # 5. Load embedding model
    model = load_embedding_model()

    # 6. Generate embeddings
    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(
        texts,
        model,
    )

    # 7. Create ChromaDB collection
    collection = create_vector_store()

    # 8. Store chunks + embeddings
    add_documents(
        collection,
        chunks,
        embeddings,
    )

    return {
        "total_files": len(all_files),
        "selected_files": len(selected_files),
        "documents": len(documents),
        "chunks": len(chunks),
        "stored_documents": collection.count(),
    }