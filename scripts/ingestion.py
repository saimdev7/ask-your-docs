from scripts.content_fetcher import load_pdf
from scripts.chunking import split_docs
from scripts.chroma_db import save_chunks   


def ingest_pdf(path, session_id):
    docs = load_pdf(path)
    chunks = split_docs(docs)
    save_chunks(chunks, session_id)
    return len(chunks)