Objetivo: 
transformar fluxos do diagrama
 (processos: PS/PU/PM, fermentações, métodos emergentes etc.)
  em agents especializados (por exemplo: FermentationAgent, DryProcessAgent, 
  NovelMethodsAgent, RAGKnowledgeAgent) que cooperam para responder perguntas, 
  propor workflows e executar ações (p.ex. persistir dados, recuperar documentos, 
  chamar ferramentas).

Camadas:

Flask UI / API — front-end leve para receber requests (web UI ou API).

Orquestrador de Agents — módulo Python que usa CrewAI para criar e executar agents colaborativos. 
Pode integrar LangChain para retriever/RAG e LangGraph para pipelines/visualização do fluxo. 
CrewAI
LangChain AI

MCP (Model Context Protocol) — expõe fontes de contexto e ferramentas 
(e.g., banco de dados com metadados do processamento, repositório de papers 
sobre maceração carbônica, endpoints para iniciar secagem). 
Agents acessam MCP servers/clients para obter contexto e acionar ferramentas. 
Use SDKs oficiais (Python SDK). 
Model Context Protocol
+1

RAG / Vector DB — LangChain + FAISS/Weaviate/Milvus 
para recuperar documentos técnicos (ex.: notas sobre "maceração carbônica"). 
LangChain AI

Infra / Container — Docker + docker-compose; VM no GCP/AWS com firewall 
liberado para as portas necessárias.

Por que MCP? Porque padroniza como agentes pedem dados e 
chamam ferramentas (é o “USB-C” entre LLMs e apps) — facilita integrar agentes com repositórios,
 bases e ferramentas sem reescrever conectores.

 # coffee-agents

Scaffold para transformar fluxos de processamento de café em agents (CrewAI + LangChain + LangGraph)
com interface Flask, Model Context Protocol (MCP) e deploy via Docker / docker-compose.

## Estrutura
Veja os arquivos e como rodar localmente.

## Como usar (local)
1. Copie `.env.example` para `.env` e preencha as chaves:
   ```bash
   cp .env.example .env
