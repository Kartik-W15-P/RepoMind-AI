import chromadb


COLLECTION_NAME = "repomind_documents"


def create_vector_store(
    persist_directory: str = "chroma_db",
):
    # Create a persistent ChromaDB client and collection.

    client = chromadb.PersistentClient(
        path=persist_directory
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def add_documents(
    collection,
    chunks: list[dict],
    embeddings: list[list[float]],
) -> None:
    # Store document chunks, embeddings, and metadata in ChromaDB.

    ids = []
    documents = []
    metadatas = []

    for index, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        ids.append(f"chunk_{index}")
        documents.append(chunk["content"])
        metadatas.append(chunk["metadata"])

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def search_documents(
    collection,
    query_embedding: list[float],
    top_k: int = 3,
):
    # Search ChromaDB for the most relevant document chunks.

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results