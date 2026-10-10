from langchain_chroma import Chroma
from scripts.vectorize import JinaEmbeddings


def save_chunks(chunks, session_id):
    print(f"Chunks to store in ChromaDB: {len(chunks)}")
    return Chroma.from_documents(
        documents=chunks,
        embedding=JinaEmbeddings(),
        collection_name=f"sess-{session_id}",
        persist_directory="chroma_db",
    )