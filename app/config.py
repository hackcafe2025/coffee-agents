import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8001")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "/data/faiss.index")
