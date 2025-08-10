☕ Coffee Agents — Agentes para a Cafeicultura Inteligente

Objetivo: Criar agentes especializados para diferentes etapas e processos da cafeicultura, capazes de cooperar entre si para:

             * Responder perguntas técnicas.
             * Propor workflows de processamento.
             * Executar ações como persistir dados, recuperar documentos, 
               chamar ferramentas de análise e muito mais.
                 
O sistema foi pensado para unir IA colaborativa, recuperação inteligente de informações e execução automatizada de tarefas, 
criando uma base sólida para apoiar produtores, pesquisadores e técnicos da cadeia do café.

Arquitetura por Camadas

    1. Flask UI / API
    
        - Interface web e API leves para receber requisições.
        - Pode servir como painel de controle ou ponto de integração 
          com sistemas externos.

    2. CrewAI — Orquestração de Agentes
    
         Núcleo Python que utiliza CrewAI para criar e executar agentes colaborativos.
         Os agentes são capazes de trocar informações, dividir tarefas e coordenar ações.
         Integração com:
               LangChain para retriever e RAG.
               LangGraph para pipelines e visualização de fluxos.

     3. LangChain
     
         Fornece a base para recuperação de contexto, integração com 
         ferramentas e bases de dados.
         Os agentes podem acessar servidores e clientes MCP para 
         buscar contexto e acionar recursos especializados.

      4. MCP (Model Context Protocol)
      
         Padrão para expor fontes de contexto e ferramentas.
         Acesso a:
                  Banco de dados com metadados de processamento.
                  Repositório de artigos e pesquisas sobre maceração carbônica, 
                  secagem, entre outros.

        💡 Por que MCP?
               Porque ele é como o “USB-C” entre LLMs e aplicações: padroniza 
               como agentes pedem dados e usam ferramentas, facilitando a integração 
               com  novas fontes sem reescrever conectores.

       5. RAG / Vector DB
       
           Implementado com LangChain para recuperação de documentos técnicos.
           Base vetorial otimizada para buscas contextuais.

       6. Infraestrutura / Deploy
       
           Contêineres Docker + docker-compose para empacotar 
           e rodar toda a aplicação. Pronto para execução local ou em nuvem.

Resumo do Projeto:

     Transformar fluxos de processamento de café em agentes inteligentes 
     (CrewAI + LangChain + LangGraph),com interface Flask, padrão Model Context Protocol (MCP)
     e deploy simplificado via Docker.

Como Rodar Localmente:

     Copie o arquivo .env.example para .env e configure as variáveis:
     
     Inicie a aplicação com Docker: docker-compose up --build
     
     Acesse a interface em: http://localhost:5000
