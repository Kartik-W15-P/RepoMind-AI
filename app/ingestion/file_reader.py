from pathlib import Path


def read_file(file_path: Path) -> str:
    """Read a text file and return its contents."""

    try:
        return file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    except OSError as error:
        raise RuntimeError(
            f"Failed to read file: {file_path}"
        ) from error


def get_file_metadata(
    file_path: Path,
    repository_path: Path,
) -> dict:
    """Create metadata for a repository file."""

    relative_path = file_path.relative_to(repository_path)

    return {
        "source": str(relative_path),
        "file_name": file_path.name,
        "file_type": file_path.suffix.lower(),
    }


def read_repository_files(
    files: list[Path],
    repository_path: Path,
) -> list[dict]:
    """Read selected repository files and attach metadata."""

    documents = []

    for file_path in files:

        content = read_file(file_path)

        if not content.strip():
            continue

        metadata = get_file_metadata(
            file_path,
            repository_path,
        )

        documents.append(
            {
                "content": content,
                "metadata": metadata,
            }
        )

    return documents