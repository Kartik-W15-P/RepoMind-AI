from pathlib import Path

from app.rag.pipeline import index_repository
from app.rag.rag_pipeline import ask_repository

repository_path = Path("data/repositories/requests")

print("Indexing repository...\n")

result = index_repository(repository_path)

print("Indexing complete:")
print(result)

print("\nAsking question...\n")

answer, sources = ask_repository(
    "What database does this project use?"
)

print("Answer:")
print(answer)

print("\nSources:")
for source in sources:
    print(f"- {source.get('source')}")