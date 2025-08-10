# requirements.txt
"""
streamlit==1.28.0
langchain==0.0.350
langchain-community==0.0.10
langchain-openai==0.0.2
faiss-cpu==1.7.4
sentence-transformers==2.2.2
PyPDF2==3.0.1
python-dotenv==1.0.0
crewai==0.1.0
openai==1.3.0
"""

import os
import streamlit as st
from dotenv import load_dotenv
import tempfile
import traceback
from typing import List, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # LangChain imports
    from langchain.document_loaders import PyPDFLoader, TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain.vectorstores import FAISS
    from langchain.chains import RetrievalQA
    from langchain.llms import OpenAI
    from langchain.prompts import PromptTemplate
    from langchain.schema import Document
    
    # Imports alternativos se CrewAI não estiver disponível
    CREWAI_AVAILABLE = True
    try:
        from crewai import Agent, Task, Crew, Process
        from crewai.tools import BaseTool
    except ImportError:
        CREWAI_AVAILABLE = False
        logger.warning("CrewAI não disponível, usando modo simplificado")
    
except ImportError as e:
    logger.error(f"Erro ao importar dependências: {e}")
    st.error(f"Erro ao importar dependências: {e}")

# Carregar variáveis de ambiente
load_dotenv()

class SimpleRAGSystem:
    """Sistema RAG simplificado sem CrewAI"""
    
    def __init__(self):
        self.vectorstore = None
        self.qa_chain = None
        self.embeddings = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
    def initialize_embeddings(self):
        """Inicializa embeddings de forma segura"""
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            return True
        except Exception as e:
            logger.error(f"Erro ao inicializar embeddings: {e}")
            return False
    
    def load_documents_from_text(self, texts: List[str], filenames: List[str]) -> List[Document]:
        """Carrega documentos de texto simples"""
        documents = []
        for text, filename in zip(texts, filenames):
            if text.strip():
                doc = Document(
                    page_content=text,
                    metadata={"source": filename}
                )
                documents.append(doc)
        return documents
    
    def create_vectorstore(self, documents: List[Document]) -> bool:
        """Cria vectorstore de forma segura"""
        try:
            if not documents:
                return False
                
            if self.embeddings is None:
                if not self.initialize_embeddings():
                    return False
            
            # Dividir documentos
            texts = self.text_splitter.split_documents(documents)
            
            # Criar vectorstore
            self.vectorstore = FAISS.from_documents(texts, self.embeddings)
            
            # Configurar QA chain
            self.setup_qa_chain()
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar vectorstore: {e}")
            return False
    
    def setup_qa_chain(self):
        """Configura QA chain"""
        try:
            if not os.getenv("OPENAI_API_KEY"):
                return False
                
            llm = OpenAI(
                temperature=0.2,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            
            template = """
            Você é um especialista em processamento de café. Use o contexto para responder a pergunta.
            
            Contexto: {context}
            
            Pergunta: {question}
            
            Resposta:
            """
            
            prompt = PromptTemplate(
                template=template,
                input_variables=["context", "question"]
            )
            
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
                chain_type_kwargs={"prompt": prompt}
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao configurar QA chain: {e}")
            return False
    
    def query(self, question: str) -> str:
        """Faz uma pergunta ao sistema"""
        try:
            if self.qa_chain is None:
                return "Sistema não configurado. Carregue documentos primeiro."
                
            result = self.qa_chain.run(question)
            return result
            
        except Exception as e:
            logger.error(f"Erro na consulta: {e}")
            return f"Erro ao processar pergunta: {str(e)}"

def create_sample_documents() -> List[Document]:
    """Cria documentos de exemplo sobre café"""
    sample_texts = [
        """
        FERMENTAÇÃO ANAERÓBICA NO CAFÉ
        
        A fermentação anaeróbica é um processo inovador no beneficiamento do café que ocorre na ausência de oxigênio.
        Este método pode durar entre 48 a 120 horas, dependendo da temperatura ambiente.
        
        Características:
        - Temperatura ideal: 15-25°C
        - Ambiente controlado sem oxigênio
        - Produz sabores mais intensos e frutados
        - Aumenta a complexidade da bebida
        
        O processo resulta em cafés com notas que lembram vinho e frutas fermentadas.
        """,
        
        """
        PROCESSO ÚMIDO VS PROCESSO SECO
        
        PROCESSO ÚMIDO:
        - Despolpamento imediato após colheita
        - Fermentação em tanques com água
        - Lavagem para remoção de mucilagem
        - Secagem do pergaminho
        - Resulta em acidez mais pronunciada
        
        PROCESSO SECO:
        - Secagem do fruto inteiro
        - Fermentação natural durante secagem
        - Remove casca após secagem completa
        - Maior corpo e doçura
        - Método tradicional mais antigo
        """,
        
        """
        CONTROLE DE TEMPERATURA NA SECAGEM
        
        A secagem é uma etapa crítica que afeta diretamente a qualidade final do café.
        
        Fatores importantes:
        - Temperatura: não deve exceder 40°C
        - Umidade relativa: 50-60%
        - Tempo: 15-30 dias dependendo do método
        - Revolvimento regular dos grãos
        
        Cuidados especiais:
        - Evitar secagem muito rápida
        - Proteger de chuva e umidade excessiva
        - Monitorar umidade final (10-12%)
        """,
        
        """
        PROCESSO HONEY (SEMI-LAVADO)
        
        O processo honey combina características dos processos úmido e seco.
        
        Etapas:
        1. Despolpamento parcial
        2. Manutenção de parte da mucilagem
        3. Secagem com mucilagem aderida
        4. Fermentação controlada durante secagem
        
        Tipos de honey:
        - White honey: menos mucilagem
        - Yellow honey: mucilagem intermediária  
        - Red honey: mais mucilagem
        - Black honey: máxima mucilagem
        
        Resultado: doçura equilibrada com acidez moderada.
        """
    ]
    
    filenames = [
        "fermentacao_anaerobica.txt",
        "processos_umido_seco.txt", 
        "controle_temperatura.txt",
        "processo_honey.txt"
    ]
    
    documents = []
    for text, filename in zip(sample_texts, filenames):
        doc = Document(page_content=text, metadata={"source": filename})
        documents.append(doc)
    
    return documents

def main():
    st.set_page_config(
        page_title="Sistema RAG para Café",
        page_icon="☕",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    try:
        st.title("☕ Sistema RAG para Processamento de Café")
        st.markdown("**LangChain + FAISS + OpenAI**")
        
        # Verificar dependências
        if not CREWAI_AVAILABLE:
            st.warning("⚠️ CrewAI não disponível. Usando modo RAG simplificado.")
        
        # Inicializar sistema
        if 'rag_system' not in st.session_state:
            st.session_state.rag_system = SimpleRAGSystem()
            st.session_state.documents_loaded = False
        
        # Sidebar
        with st.sidebar:
            st.header("📚 Documentos")
            
            # Opção para usar documentos de exemplo
            if st.button("📄 Carregar Documentos de Exemplo"):
                with st.spinner("Carregando documentos de exemplo..."):
                    sample_docs = create_sample_documents()
                    success = st.session_state.rag_system.create_vectorstore(sample_docs)
                    
                    if success:
                        st.session_state.documents_loaded = True
                        st.success("✅ Documentos de exemplo carregados!")
                        st.info(f"Carregados {len(sample_docs)} documentos sobre café")
                    else:
                        st.error("❌ Erro ao carregar documentos")
            
            # Upload de arquivos personalizados
            st.subheader("📤 Upload Personalizado")
            uploaded_files = st.file_uploader(
                "Carregar seus documentos",
                accept_multiple_files=True,
                type=['txt', 'pdf']
            )
            
            if uploaded_files and st.button("🔄 Processar Uploads"):
                with st.spinner("Processando uploads..."):
                    try:
                        documents = []
                        for uploaded_file in uploaded_files:
                            content = uploaded_file.getvalue().decode('utf-8')
                            doc = Document(
                                page_content=content,
                                metadata={"source": uploaded_file.name}
                            )
                            documents.append(doc)
                        
                        if documents:
                            success = st.session_state.rag_system.create_vectorstore(documents)
                            if success:
                                st.session_state.documents_loaded = True
                                st.success(f"✅ {len(documents)} documentos processados!")
                            else:
                                st.error("❌ Erro ao processar documentos")
                    except Exception as e:
                        st.error(f"Erro no upload: {str(e)}")
            
            # Status
            st.subheader("📊 Status")
            if st.session_state.documents_loaded:
                st.success("✅ Documentos carregados")
            else:
                st.warning("⏳ Carregue documentos primeiro")
                
            if os.getenv("OPENAI_API_KEY"):
                st.success("✅ API Key configurada")
            else:
                st.error("❌ Configure OPENAI_API_KEY")
        
        # Área principal
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("💬 Faça sua Pergunta")
            
            # Perguntas de exemplo
            st.subheader("🎯 Exemplos:")
            examples = [
                "Como funciona a fermentação anaeróbica?",
                "Qual a diferença entre processo úmido e seco?",
                "Como controlar a temperatura na secagem?",
                "O que é processo honey?"
            ]
            
            selected_example = st.selectbox("Escolha um exemplo:", [""] + examples)
            
            # Input da pergunta
            question = st.text_area(
                "Sua pergunta:",
                value=selected_example,
                height=100,
                placeholder="Digite sua pergunta sobre processamento de café..."
            )
            
            # Botão de consulta
            if st.button("🚀 Consultar", type="primary"):
                if not question.strip():
                    st.error("❌ Digite uma pergunta!")
                elif not st.session_state.documents_loaded:
                    st.error("❌ Carregue documentos primeiro!")
                elif not os.getenv("OPENAI_API_KEY"):
                    st.error("❌ Configure sua OPENAI_API_KEY no arquivo .env")
                else:
                    with st.spinner("🤔 Processando..."):
                        try:
                            response = st.session_state.rag_system.query(question)
                            
                            st.success("✅ Resposta gerada!")
                            st.markdown("### 📋 Resposta:")
                            st.markdown(response)
                            
                        except Exception as e:
                            st.error(f"❌ Erro: {str(e)}")
                            st.error("Verifique se a OPENAI_API_KEY está correta")
        
        with col2:
            st.header("ℹ️ Como Usar")
            
            st.markdown("""
            **Passos:**
            
            1️⃣ **Configure API Key**
            ```
            # Crie arquivo .env
            OPENAI_API_KEY=sk-...
            ```
            
            2️⃣ **Carregue Documentos**
            - Use exemplos prontos, ou
            - Faça upload de TXT/PDF
            
            3️⃣ **Faça Perguntas**
            - Use exemplos ou digite
            - Clique "Consultar"
            
            4️⃣ **Veja Resultados**
            - Resposta baseada nos docs
            - Informação contextualizada
            """)
            
            st.header("🔧 Tecnologias")
            st.markdown("""
            - **LangChain**: Pipeline RAG
            - **FAISS**: Busca vetorial  
            - **HuggingFace**: Embeddings
            - **OpenAI**: Geração de texto
            - **Streamlit**: Interface web
            """)
            
            st.header("📊 Arquitetura")
            st.markdown("""
            ```
            Documentos → Chunking → 
            Embeddings → FAISS → 
            Retrieval → OpenAI → 
            Resposta
            ```
            """)
    
    except Exception as e:
        st.error("❌ Erro na aplicação:")
        st.error(str(e))
        st.error("Verifique se todas as dependências estão instaladas")
        
        with st.expander("🐛 Detalhes do Erro"):
            st.code(traceback.format_exc())

if __name__ == "__main__":
    # Verificação inicial
    try:
        main()
    except Exception as e:
        st.error(f"Erro crítico: {str(e)}")
        st.info("Recarregue a página ou verifique as dependências")

# Script de instalação das dependências
install_script = '''
#!/bin/bash
echo "Instalando dependências do RAG..."
pip install streamlit==1.28.0
pip install langchain==0.0.350
pip install langchain-community==0.0.10
pip install langchain-openai==0.0.2
pip install faiss-cpu==1.7.4
pip install sentence-transformers==2.2.2
pip install PyPDF2==3.0.1
pip install python-dotenv==1.0.0
pip install openai==1.3.0
echo "Instalação concluída!"
'''