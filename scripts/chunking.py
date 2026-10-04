import sys
from langchain_text_splitters import RecursiveCharacterTextSplitter
from scripts.content_fetcher import load_pdf


def split_docs(docs, chunk_size=200, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(docs)


if __name__ == "__main__":
    docs = load_pdf(sys.argv[1])
    chunks = split_docs(docs)

    print(f"Pages: {len(docs)}")
    print(f"Chunks: {len(chunks)}")
