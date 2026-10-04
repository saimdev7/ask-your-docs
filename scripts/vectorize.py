import os
import requests
from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings

load_dotenv()


class JinaEmbeddings(Embeddings):
    def _embed(self, texts, task):
        response = requests.post(
            "https://api.jina.ai/v1/embeddings",
            headers={"Authorization": f"Bearer {os.getenv('JINA_API_KEY')}"},
            json={"model": os.getenv("JINA_MODEL"), "task": task, "input": texts},
        )
        response.raise_for_status()
        return [item["embedding"] for item in response.json()["data"]]

    def embed_documents(self, texts):
        return self._embed(texts, "retrieval.passage")

    def embed_query(self, text):
        return self._embed([text], "retrieval.query")[0]