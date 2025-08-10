# retriever minimal para RAG (stub). Substitua por LangChain + FAISS/Weaviate
import os
from config import VECTOR_DB_PATH

class Retriever:
    def __init__(self, index_path=VECTOR_DB_PATH):
        self.index_path = index_path

    def query(self, text, k=3):
        # stub — em produção: buscar no vector store e retornar documentos
        return [
            {"source": "paper1.pdf", "text": f"Conteúdo sobre {text} - trecho 1"},
            {"source": "paper2.pdf", "text": f"Conteúdo sobre {text} - trecho 2"},
        ]
