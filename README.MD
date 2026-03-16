# Praxa 🎭

A RAG-powered chatbot for answering questions about West End and Broadway theatre. Praxa combines a curated PDF knowledge base with a retrieval-augmented generation pipeline to provide accurate, source-backed answers about shows, productions, venues, and the people behind them.

---

## Features

- Conversational chat interface built with Streamlit
- Retrieval-Augmented Generation (RAG) — answers are grounded in your own documents, not just LLM training data
- Source citations with every answer (filename + page number)
- Local embeddings via `all-MiniLM-L6` — no API call needed for indexing
- Powered by `gemma-3-27b` via OpenRouter

---

## Tech Stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| LLM Orchestration | LangChain |
| LLM | `gemma-3-27b` via OpenRouter |
| Embedding Model | `all-MiniLM-L6-v2` (sentence-transformers) |
| Vector Database | Chroma |
| Document Loader | LangChain PyPDFLoader |
| Text Splitting | RecursiveCharacterTextSplitter |

---

## Project Structure

```
Praxa/
├── praxa_client.py     # Streamlit UI — chat interface
├── praxa_rag.py        # RAG chain — retrieval, prompt, LLM, sources
├── context.py          # Chroma vector store setup and PDF indexing
├── model.py            # OpenRouter LLM initialisation
├── data/               # PDF documents (your knowledge base)
├── chroma_db/          # Persisted Chroma vector index (auto-generated)
└── requirements.txt
```

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/praxa.git
cd praxa
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your OpenRouter API key

Create a `.env` file in the project root:

```
OPENROUTER_API_KEY=your_api_key_here
```

You can get a free API key at [openrouter.ai](https://openrouter.ai).

### 5. Add your PDF documents


Place the following PDFs inside a `context_data/` directory:

- `westend_2025.pdf` — plays and musicals coming to the West End in 2025
- `broadway_longest_running.pdf` — longest-running shows in Broadway history

> These files are provided via the course repository. If you are a student
> on this course, download them from your school's repo and place them here.
> External users will need to substitute their own theatre reference PDFs.

### 6. Build the vector index

Run the context module once to embed your PDFs and populate the Chroma database:

```bash
python context.py
```

This only needs to be done once, or again whenever you add new documents.

---

## Running the App

```bash
streamlit run praxa_client.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## How the RAG Pipeline Works

```
User question
      │
      ▼
 Embed question           ← all-MiniLM-L6-v2
      │
      ▼
 Similarity search        ← Chroma finds top-k most relevant chunks
      │
      ▼
 Build prompt             ← LangChain formats question + retrieved context
      │
      ▼
 LLM generates answer     ← gemma-3-27b via OpenRouter
      │
      ▼
 Return answer + sources  ← filename and page number for each chunk used
```

At indexing time, each PDF is loaded, split into overlapping chunks using `RecursiveCharacterTextSplitter`, and embedded using `all-MiniLM-L6-v2`. The resulting vectors are stored in a local Chroma database alongside the original text and metadata.

At query time, the user's question is embedded using the same model, and Chroma performs a cosine similarity search to retrieve the most relevant chunks. These are passed to `gemma-3-27b` as context alongside the question, and the model generates a grounded answer. The source documents are returned alongside the answer so the user can verify the information.

---

## Requirements

```
streamlit
langchain
langchain-community
langchain-chroma
langchain-openai
sentence-transformers
chromadb
pypdf
python-dotenv
```

---