# 🧠 RepoMind AI

> **GitHub Repository Intelligence & Codebase Understanding Assistant**

RepoMind AI is a Retrieval-Augmented Generation (RAG) application that allows users to connect a public GitHub repository and ask questions about its codebase, documentation, configuration, and project structure.

Instead of relying only on an LLM's general knowledge, RepoMind retrieves relevant content directly from the repository and provides it as context to the language model before generating an answer.

---

## 🚀 Features

- Connect any public GitHub repository
- Automatically clone and inspect repositories
- Filter relevant source-code and documentation files
- Split repository content into searchable chunks
- Generate semantic embeddings using Sentence Transformers
- Store embeddings in ChromaDB
- Retrieve relevant repository context for user questions
- Generate grounded answers using Hugging Face-hosted Qwen
- Display source files used for the answer
- Avoid unsupported answers when repository context is insufficient
- Interactive Streamlit interface

---

## 🏗️ Architecture

```text
USER
  │
  ▼
Streamlit UI
  │
  ▼
GitHub Repository
  │
  ▼
Repository Ingestion
  │
  ▼
File Filtering
  │
  ▼
File Reading
  │
  ▼
Chunking
  │
  ▼
Embeddings
  │
  ▼
ChromaDB
  │
  │
  └──────── User Question
             │
             ▼
       Query Embedding
             │
             ▼
      Semantic Retrieval
             │
             ▼
   Relevant Repository Context
             │
             ▼
          Qwen LLM
             │
             ▼
       Grounded Answer
             │
             ▼
       Source References
````

---

## 🔄 How It Works

RepoMind AI follows a Retrieval-Augmented Generation pipeline.

### 1. Connect Repository

The user provides a public GitHub repository URL.

Example:

```text
https://github.com/psf/requests
```

### 2. Clone Repository

RepoMind uses Git to clone the repository locally.

### 3. Filter Files

Only relevant repository content is selected.

Currently supported content includes:

* Python
* JavaScript
* TypeScript
* Java
* C/C++
* Markdown
* Text
* JSON
* YAML
* TOML
* Common project configuration files

Unnecessary directories such as `.git`, virtual environments, caches, `node_modules`, build directories, and distribution directories are ignored.

### 4. Read Files

Selected files are read and stored with metadata such as:

* File path
* File name
* File type

### 5. Chunk Documents

Large documents are split into smaller chunks using LangChain's `RecursiveCharacterTextSplitter`.

Current configuration:

```text
Chunk size:    1000 characters
Chunk overlap: 150 characters
```

### 6. Generate Embeddings

Each chunk is converted into a semantic vector using:

```text
sentence-transformers
all-MiniLM-L6-v2
```

The resulting embeddings have 384 dimensions.

### 7. Store in ChromaDB

The chunks, embeddings, and metadata are stored in a persistent ChromaDB collection.

### 8. Retrieve Relevant Context

When a user asks a question, the question is converted into an embedding and compared against the repository chunks.

The most relevant chunks are retrieved.

### 9. Generate Answer

The retrieved repository context is sent to the Qwen language model through Hugging Face Inference.

The model is instructed to answer using only the supplied repository context.

### 10. Display Sources

RepoMind displays the repository files associated with the retrieved context.

---

## 🛠️ Tech Stack

| Component            | Technology                     |
| -------------------- | ------------------------------ |
| Programming Language | Python                         |
| User Interface       | Streamlit                      |
| RAG                  | LangChain                      |
| Text Splitting       | RecursiveCharacterTextSplitter |
| Embeddings           | Sentence Transformers          |
| Embedding Model      | `all-MiniLM-L6-v2`             |
| Vector Database      | ChromaDB                       |
| LLM                  | Qwen3-4B-Instruct-2507         |
| LLM Provider         | Hugging Face Inference         |
| Repository Access    | Git                            |
| Version Control      | Git / GitHub                   |

---

## 📁 Project Structure

```text
RepoMind-AI/
│
├── app/
│   ├── ingestion/
│   │   ├── chunker.py
│   │   ├── file_filter.py
│   │   ├── file_reader.py
│   │   └── github_loader.py
│   │
│   └── rag/
│       ├── embeddings.py
│       ├── generator.py
│       ├── pipeline.py
│       ├── rag_pipeline.py
│       └── vector_store.py
│
├── streamlit_app.py
├── test_generator.py
├── test_huggingface.py
├── test_rag.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Kartik-W15-P/RepoMind-AI.git
cd RepoMind-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

RepoMind uses a Hugging Face access token for LLM inference.

Create a `.env` file in the project root:

```env
HF_TOKEN=your_huggingface_token
```

You can use `.env.example` as a template.

> **Important:** Never commit your `.env` file or expose your Hugging Face token publicly.

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run streamlit_app.py
```

The application allows you to:

1. Enter a public GitHub repository URL.
2. Index the repository.
3. Ask questions about the codebase.
4. View the generated answer.
5. Inspect the source files used for retrieval.

---

## 💬 Example Questions

After indexing a repository, you can ask:

```text
What is this project used for?
```

```text
How is the project structured?
```

```text
Where is authentication implemented?
```

```text
Where is the main Session class implemented?
```

```text
What technologies does this project use?
```

```text
How does this endpoint work?
```

```text
Which files handle database operations?
```

---

## 🧪 Testing

RepoMind was tested using both its own repository and a real-world open-source repository.

### Tested Repository

```text
psf/requests
```

The system successfully processed:

```text
158 total files
65 selected files
64 readable documents
684 knowledge chunks
684 stored vector documents
```

### Code Understanding Test

Question:

```text
Where is the main Session class implemented?
```

RepoMind correctly identified:

```text
src/requests/sessions.py
```

### Grounding Test

For an unsupported question such as:

```text
What database does this project use?
```

RepoMind returned:

```text
I couldn't find enough information in the repository context.
```

This demonstrates that the system can avoid generating an unsupported answer when the retrieved repository context does not contain sufficient information.

---

## 🛡️ Grounded RAG

A key design goal of RepoMind is to reduce unsupported LLM responses.

The generation prompt instructs the model to:

* Use only retrieved repository context.
* Avoid inventing files or implementation details.
* Mention relevant source files when available.
* Explicitly state when the repository context is insufficient.

---

## ⚠️ Current Limitations

RepoMind AI is currently an MVP.

Current limitations include:

* Only public GitHub repositories are supported.
* Retrieval is primarily semantic.
* Large repositories may require more indexing time.
* Dependency and configuration retrieval is not always perfect.
* Code is currently chunked primarily by text rather than programming-language structure.
* No advanced code dependency graph is currently implemented.
* Private repository support is not currently included.
* LLM responses depend on the quality of retrieved context and the hosted inference model.

---

## 🔮 Future Improvements

Potential future improvements include:

* AST-based code-aware chunking
* Hybrid semantic + keyword retrieval
* Retrieval reranking
* Code dependency and impact analysis
* Repository architecture visualization
* Private GitHub repository support
* GitHub API integration
* Conversation memory
* Automated RAG evaluation
* More advanced code search
* Deployment and monitoring

---

## 🎯 Project Goal

RepoMind AI explores how Retrieval-Augmented Generation can be applied to software engineering workflows.

The goal is to make large or unfamiliar codebases easier to understand by combining:

```text
Repository Data
      +
Semantic Retrieval
      +
Large Language Model
      =
Codebase Intelligence Assistant
```

---

## 👨‍💻 Author

**Kartik**

GitHub:

[https://github.com/Kartik-W15-P](https://github.com/Kartik-W15-P)
