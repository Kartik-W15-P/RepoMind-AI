from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_text_splitter() -> RecursiveCharacterTextSplitter:
    # Create the text splitter used by RepoMind AI."""

    return RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            " ",
            "",
        ],
    )


def chunk_documents(documents: list[dict]) -> list[dict]:
    # Split repository documents into smaller chunks.

    text_splitter = create_text_splitter()

    chunks = []

    for document in documents:

        split_texts = text_splitter.split_text(
            document["content"]
        )

        for index, text in enumerate(split_texts):

            chunk_metadata = document["metadata"].copy()

            chunk_metadata["chunk_index"] = index

            chunks.append(
                {
                    "content": text,
                    "metadata": chunk_metadata,
                }
            )

    return chunks