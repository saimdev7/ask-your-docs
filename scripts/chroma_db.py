import sys
from langchain_chroma import Chroma
from scripts.vectorize import JinaEmbeddings
from scripts.content_fetcher import load_pdf
from scripts.chunking import split_docs


def save_chunks(chunks, session_id):
    return Chroma.from_documents(
        documents=chunks,
        embedding=JinaEmbeddings(),
        collection_name=f"sess-{session_id}",
        persist_directory="chroma_db",
    )


if __name__ == "__main__":
    docs = load_pdf(sys.argv[1])
    chunks = split_docs(docs)
    vector_store = save_chunks(chunks, "test")

    print(f"Chunks : {len(chunks)}")
    print(f"Chunks Store in chroma : {vector_store._collection.count()}")