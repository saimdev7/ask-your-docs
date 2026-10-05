# Ask Your Docs

A RAG web app to chat with your PDFs. Upload a document, ask questions, and get answers grounded only in that document, streamed token by token.

Built with FastAPI, LangChain, ChromaDB, Jina embeddings and Groq.

## Features

- PDF upload with per-session isolation: each browser session gets its own Chroma collection
- Retrieval-augmented answers that refuse to guess ("I don't know" when the context has no answer)
- Streaming responses over HTTP
- Minimal HTML/CSS/JS frontend served by the same FastAPI app

## How it works

```
Upload   PDF -> load -> split into chunks -> embed (Jina) -> store in Chroma (collection per session)

Query    question -> embed -> top-k similar chunks -> prompt + context -> LLM (Groq) -> streamed answer
```

## Tech stack

| Layer | Choice |
|---|---|
| Backend | FastAPI |
| Orchestration | LangChain (LCEL) |
| LLM | Groq |
| Embeddings | Jina embeddings (API) |
| Vector store | ChromaDB (persistent, local) |
| Frontend | HTML, CSS, JavaScript |

## Project structure

```
admin/
  main.py              FastAPI app and routes
scripts/               ingestion pipeline
  content_fetcher.py   PDF loading
  chunking.py          text splitting
  vectorize.py         Jina embeddings wrapper
  chroma_db.py         vector store
  ingestion.py         load -> split -> embed -> store
services/
  query_service.py     retrieval and answer generation
static/
  index.html           chat UI
```

## Getting started

**Prerequisites:** Python 3.10+, a [Groq](https://console.groq.com/keys) API key, a [Jina](https://jina.ai/embeddings) API key.

```bash
git clone https://github.com/saimdev7/ask-your-docs.git
cd ask-your-docs

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp env.example .env      # then add your API keys
uvicorn admin.main:app --reload
```

Open http://127.0.0.1:8000, upload a PDF, and start asking.

## Configuration

Set in `.env`:

| Variable | Description |
|---|---|
| `JINA_API_KEY` | Jina API key |
| `JINA_MODEL` | Embedding model, e.g. `jina-embeddings-v5-text-small` |
| `GROQ_API_KEY` | Groq API key |
| `GROQ_MODEL` | Chat model, e.g. `openai/gpt-oss-20b` |

Model availability on free tiers changes. If you get a `model_not_found` error, pick another model from your Groq console.

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Chat UI |
| `GET` | `/health` | Health check |
| `POST` | `/upload` | Form data: `session_id`, `file` (PDF). Ingests the document |
| `POST` | `/chat` | JSON: `{"question", "session_id"}`. Streams the answer as plain text |

Interactive docs are available at `/docs`.

## Limitations

- No authentication; sessions are identified by a client-generated ID
- Uploading a second PDF in the same session adds to the existing collection instead of replacing it
- Storage is local (`chroma_db/`, `uploads/`), so a deployment needs a persistent disk
