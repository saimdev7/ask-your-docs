import sys
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(path):
    return PyPDFLoader(path).load()


if __name__ == "__main__":
    docs = load_pdf(sys.argv[1])
    