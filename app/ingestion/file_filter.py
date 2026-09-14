from pathlib import Path

#This is our allowlist.
SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
}

SUPPORTED_FILENAMES = {
    "requirements.txt",
    "package.json",
    "README",
    "README.md",
}

#Ignored directories that we don't want to process.
IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "dist",
    "build",
}


def is_supported_file(file_path: Path) -> bool:
    """Check whether a file should be included in the RAG pipeline."""

    if file_path.name in SUPPORTED_FILENAMES:
        return True

    return file_path.suffix.lower() in SUPPORTED_EXTENSIONS


def is_inside_ignored_directory(
    file_path: Path,
    repository_path: Path,
) -> bool:
    """Check whether a file is inside an ignored directory."""

    relative_path = file_path.relative_to(repository_path)

    return any(
        part in IGNORED_DIRECTORIES
        for part in relative_path.parts[:-1]
    )


def filter_repository_files(
    files: list[Path],
    repository_path: Path,
) -> list[Path]:
    """Return only files relevant to the RAG pipeline."""

    filtered_files = []

    for file_path in files:

        if is_inside_ignored_directory(
            file_path,
            repository_path,
        ):
            continue

        if not is_supported_file(file_path):
            continue

        filtered_files.append(file_path)

    return filtered_files


def display_filtered_files(
    files: list[Path],
    repository_path: Path,
) -> None:
    """Display the files selected for RAG processing."""

    print("\nSelected Files")
    print("--------------")

    for file_path in files:
        relative_path = file_path.relative_to(repository_path)
        print(f"  ✓ {relative_path}")

    print(f"\nSelected files: {len(files)}")