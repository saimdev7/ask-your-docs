import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from scripts.vectorize import JinaEmbeddings

load_dotenv()

embeddings = JinaEmbeddings()

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL"),
    temperature=0
)

prompt_template = ChatPromptTemplate.from_template(
    """Answer the question using only the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question: {question}"""
)


def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


def build_chain(session_id):
    vectorstore = Chroma(
        collection_name=f"sess-{session_id}",
        persist_directory="chroma_db",
        embedding_function=embeddings,
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )

def answer_query(question, session_id):
    return build_chain(session_id).invoke(question)

def stream_answer(question, session_id):
    for token in build_chain(session_id).stream(question):
        yield token

if __name__ == "__main__":
    q = input("Question: ")
    print("Answer:", answer_query(q, "test1"))