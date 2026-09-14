import streamlit as st

from app.rag.rag_pipeline import ask_repository
from app.rag.pipeline import index_repository
from app.ingestion.github_loader import (
    clone_repository,
    get_repository_name,
)


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="RepoMind AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Main application */
    .stApp {
        background: #0b0f19;
    }

    /* Header */
    .main-header {
        padding: 1.5rem 0 1rem 0;
    }

    .brand {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }

    .tagline {
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Cards */
    .metric-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        min-height: 105px;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
    }

    .metric-label {
        color: #9ca3af;
        font-size: 0.85rem;
        margin-top: 0.25rem;
    }

    /* Section titles */
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }

    /* Answer card */
    .answer-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 1.4rem;
        line-height: 1.7;
    }

    /* Source cards */
    .source-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        font-family: monospace;
        font-size: 0.85rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #080c14;
        border-right: 1px solid #1f2937;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 42px;
    }

    /* Input */
    .stTextInput input,
    .stTextArea textarea {
        border-radius: 9px;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "indexed" not in st.session_state:
    st.session_state.indexed = False

if "repository_path" not in st.session_state:
    st.session_state.repository_path = None

if "repository_stats" not in st.session_state:
    st.session_state.repository_stats = {}

if "answer" not in st.session_state:
    st.session_state.answer = None

if "sources" not in st.session_state:
    st.session_state.sources = []


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.markdown("## ◈ RepoMind AI")

    st.caption("GitHub Repository Intelligence")

    st.divider()

    st.markdown("### How it works")

    st.markdown(
        """
        **1. Connect**

        Provide a public GitHub repository.

        **2. Index**

        RepoMind reads and indexes useful code and documentation.

        **3. Ask**

        Ask questions about the codebase.

        **4. Understand**

        Get answers grounded in the repository.
        """
    )

    st.divider()

    st.markdown("### Technology")

    st.caption("Python")
    st.caption("Streamlit")
    st.caption("LangChain")
    st.caption("Sentence Transformers")
    st.caption("ChromaDB")
    st.caption("Hugging Face")


# ---------------------------------------------------------
# Main header
# ---------------------------------------------------------

st.markdown(
    """
    <div class="main-header">
        <div class="brand">◈ RepoMind AI</div>
        <div class="tagline">
            GitHub Repository Intelligence & Codebase Understanding Assistant
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Repository section
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Connect a GitHub repository</div>',
    unsafe_allow_html=True,
)

repo_url = st.text_input(
    "GitHub repository URL",
    placeholder="https://github.com/username/repository",
    label_visibility="collapsed",
)

index_button = st.button(
    "Index Repository",
    type="primary",
    use_container_width=True,
)


if index_button:

    if not repo_url.strip():

        st.warning("Please enter a GitHub repository URL.")

    else:

        try:

            with st.spinner("Cloning and indexing repository..."):

                repository_name = get_repository_name(repo_url)

                repository_path = clone_repository(
                    repo_url,
                    destination="data/repositories",
                )

                stats = index_repository(repository_path)

                st.session_state.indexed = True
                st.session_state.repository_path = repository_path
                st.session_state.repository_stats = stats
                st.session_state.answer = None
                st.session_state.sources = []

            st.success(
                f"Repository **{repository_name}** indexed successfully."
            )

        except Exception as error:

            st.error(f"Indexing failed: {error}")


# ---------------------------------------------------------
# Repository statistics
# ---------------------------------------------------------

if st.session_state.indexed:

    stats = st.session_state.repository_stats

    st.markdown(
        '<div class="section-title">Repository overview</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        (
            col1,
            stats.get("total_files", 0),
            "Total files",
        ),
        (
            col2,
            stats.get("selected_files", 0),
            "Indexed files",
        ),
        (
            col3,
            stats.get("documents", 0),
            "Documents",
        ),
        (
            col4,
            stats.get("chunks", 0),
            "Knowledge chunks",
        ),
    ]

    for column, value, label in metrics:

        with column:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------
# Question section
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Ask your repository</div>',
    unsafe_allow_html=True,
)

question = st.text_area(
    "Repository question",
    placeholder=(
        "Examples:\n"
        "• What is this project and how does it work?\n"
        "• Where is authentication implemented?\n"
        "• Which files handle database operations?\n"
        "• Explain the main application flow."
    ),
    height=130,
    label_visibility="collapsed",
)

ask_button = st.button(
    "Ask RepoMind →",
    type="primary",
    use_container_width=True,
)


if ask_button:

    if not st.session_state.indexed:

        st.warning("Please index a repository first.")

    elif not question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner("Searching the codebase and generating answer..."):

                answer, sources = ask_repository(
                    question=question,
                    top_k=3,
                )

                st.session_state.answer = answer
                st.session_state.sources = sources

        except Exception as error:

            st.error(f"Unable to answer the question: {error}")


# ---------------------------------------------------------
# Answer
# ---------------------------------------------------------

if st.session_state.answer:

    st.markdown(
        '<div class="section-title">Answer</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="answer-card">
            {st.session_state.answer}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # Sources
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">Sources</div>',
        unsafe_allow_html=True,
    )

    unique_sources = []

    for source in st.session_state.sources:

        file_source = source.get("source", "Unknown")

        if file_source not in unique_sources:
            unique_sources.append(file_source)

    source_columns = st.columns(
        min(len(unique_sources), 3)
        if unique_sources
        else 1
    )

    for index, source in enumerate(unique_sources):

        with source_columns[index % len(source_columns)]:

            st.markdown(
                f"""
                <div class="source-card">
                    📄 {source}
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.caption(
    "RepoMind AI • Retrieval-Augmented Generation for GitHub repositories"
)