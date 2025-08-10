# agents.py - orquestrador simples usando LLM + MCP client + retriever
import asyncio
from config import OPENAI_API_KEY
from mcp_client import mcp_client
from rag.retriever import Retriever
import requests
import os

# NOTE: aqui eu uso chamadas simples ao OpenAI via requests só como exemplo.
# Substitua pelo SDK/langchain que preferir.

OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"

class FermentationAgent:
    def __init__(self):
        self.retriever = Retriever()

    def _call_llm(self, system_prompt, user_prompt):
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        body = {
            "model": "gpt-4o-mini",  # ajuste conforme provider
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 800
        }
        r = requests.post(OPENAI_CHAT_URL, headers=headers, json=body, timeout=30)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]

    def analyze(self, topic: str):
        docs = self.retriever.query(topic)
        notes = "\n".join([d["text"] for d in docs])
        system = "Você é um especialista em processamento de café e fermentações."
        user = f"Analise o tópico '{topic}'. Use estas notas:\n{notes}\nForneça um sumário técnico e recomendações práticas (3 passos)."
        return self._call_llm(system, user)

    def start_drying(self, job_id: str, temp: float = 35.0):
        # chama ferramenta no MCP
        return mcp_client.call_tool("start_drying", {"job_id": job_id, "temp": temp})

class Orchestrator:
    def __init__(self):
        self.fermentation_agent = FermentationAgent()

    def run_analysis(self, topic: str):
        return self.fermentation_agent.analyze(topic)

    def run_action_start_drying(self, job_id: str, temp: float = 35.0):
        return self.fermentation_agent.start_drying(job_id, temp)