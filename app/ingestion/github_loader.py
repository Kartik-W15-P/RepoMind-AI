import subprocess #Python needs to communicate with the operating system.
from pathlib import Path #Path gives us a clean way to work with folders and files.
from urllib.parse import urlparse #Help to examine the GitHub URL.
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from app.ingestion.file_filter import filter_repository_files


def validate_github_url(repo_url: str) -> bool:
    """Validate that the URL points to a GitHub repository."""

    parsed_url = urlparse(repo_url)

    return (
        parsed_url.scheme in {"http", "https"}
        and parsed_url.netloc == "github.com"
        and len(parsed_url.path.strip("/").split("/")) >= 2
    )


def get_repository_name(repo_url: str) -> str:
    """Extract the repository name from a GitHub URL."""

    repository_name = repo_url.rstrip("/").split("/")[-1]

    if repository_name.endswith(".git"):
        repository_name = repository_name[:-4]

    return repository_name


def clone_repository(repo_url: str, destination: str = "data/repositories") -> Path:
    """Clone a public GitHub repository locally."""

    if not validate_github_url(repo_url):
        raise ValueError("Invalid GitHub repository URL.")

    repository_name = get_repository_name(repo_url)

    destination_path = Path(destination)
    destination_path.mkdir(parents=True, exist_ok=True)

    repository_path = destination_path / repository_name

    if repository_path.exists():
        print(f"Repository already exists: {repository_path}")
        return repository_path

    print(f"Cloning repository: {repo_url}")

    try:
        subprocess.run(
            ["git", "clone", repo_url, str(repository_path)],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        raise RuntimeError("Failed to clone the GitHub repository.") from error

    print(f"Repository cloned successfully: {repository_path}")

    return repository_path


def get_repository_files(repository_path: Path) -> list[Path]:
    """Return all files inside the cloned repository."""

    files = []

    for path in repository_path.rglob("*"):
        if path.is_file():
            files.append(path)

    return files


def inspect_repository(repository_path: Path) -> None:
    """Display basic information about the repository."""

    all_files = get_repository_files(repository_path)

    selected_files = filter_repository_files(
        all_files,
        repository_path,
    )

    print("\nRepository Information")
    print("----------------------")
    print(f"Repository:     {repository_path.name}")
    print(f"Location:       {repository_path}")
    print(f"Total files:    {len(all_files)}")
    print(f"Selected files: {len(selected_files)}")
    print(f"Ignored files:  {len(all_files) - len(selected_files)}")

    print("\nSelected Files:")

    for file_path in selected_files:
        relative_path = file_path.relative_to(repository_path)
        print(f"  ✓ {relative_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage:")
        print("python -m app.ingestion.github_loader <github_repository_url>")
        raise SystemExit(1)

    repository_url = sys.argv[1]

    repository_path = clone_repository(repository_url)

    inspect_repository(repository_path)