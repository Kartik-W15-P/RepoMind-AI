# RepoMind AI

> **GitHub Repository Intelligence & Codebase Understanding Assistant**

RepoMind AI is a **RAG-powered AI assistant** that helps developers understand unfamiliar GitHub repositories by asking questions in natural language.

Instead of manually searching through files, users can provide a public GitHub repository URL and ask questions such as:

- Where is authentication implemented?
- Where is the `Session` class?
- How does this API endpoint work?
- Which files handle database operations?

## How It Works

```text
GitHub Repository
       ↓
File Filtering & Reading
       ↓
Text Chunking
       ↓
Embeddings
       ↓
ChromaDB
       ↓
Semantic Retrieval
       ↓
Qwen LLM
       ↓
Grounded Answer + Sources
```

The system retrieves relevant repository content before generating an answer, helping reduce hallucinations and keeping responses grounded in the actual codebase.


## Project Goal

To build a practical **AI Engineer / Generative AI application** demonstrating repository ingestion, embeddings, vector search, Retrieval-Augmented Generation, LLM integration, grounding, and an interactive AI interface.
