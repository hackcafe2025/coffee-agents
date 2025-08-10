import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings  # Pode trocar por HuggingFaceEmbeddings

# Caminho para os PDFs
PDF_FOLDER = "data/"
VECTORSTORE_PATH = "vectorstore/db_faiss"

def ingest():
    docs = []
    for file in os.listdir(PDF_FOLDER):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(PDF_FOLDER, file))
            docs.extend(loader.load())

    # Dividir textos em pedaços menores
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    documents = text_splitter.split_documents(docs)

    # Criar embeddings
    embeddings = OpenAIEmbeddings()  # Pode trocar por HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Criar FAISS vector store
    db = FAISS.from_documents(documents, embeddings)
    db.save_local(VECTORSTORE_PATH)

    print(f"[OK] Ingestão concluída. Vetores salvos em {VECTORSTORE_PATH}")

if __name__ == "__main__":
    ingest()
