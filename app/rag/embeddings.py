from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def load_embedding_model() -> SentenceTransformer:
    # Load the embedding model used by RepoMind AI.

    return SentenceTransformer(MODEL_NAME)


def generate_embedding(
    text: str,
    model: SentenceTransformer,
) -> list[float]:
    # Generate an embedding vector for a piece of te"""

    vector = model.encode(text)

    return vector.tolist()


def generate_embeddings(
    texts: list[str],
    model: SentenceTransformer,
) -> list[list[float]]:
    # Generate embedding vectors for multiple text

    vectors = model.encode(texts)

    return vectors.tolist()