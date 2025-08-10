import os

# Lista de todos os blocos/quadros do diagrama
# A chave será usada para a rota e o nome do arquivo HTML.
diagram_blocks = {
    "colheita": "Colheita",
    "classificacao": "Classificação",
    "cerejas_cafe": "Cerejas de café",
    "maceracao_carbonica": "Maceração Carbônica",
    "fermentacao_anaerobica": "Fermentação Anaeróbica",
    "digestao_animal": "Digestão Animal",
    "excrecao": "Excreção",
    "lavagem_digestao": "Lavagem",
    "descascamento_umido": "Descascamento Úmido",
    "secagem_umido": "Secagem",
    "graos_pergaminho_seco": "Grãos de café em pergaminho seco",
    "descascamento_seco": "Descascamento",
    "graos_cafe_verde": "Grãos de café verde",
    "fermentacao_microbiana": "Fermentação microbiana / enzimática",
    "secagem_final": "Secagem",
    "processo_seco": "Processo Seco (PS)",
    "cerejas_secas": "Cerejas Secas",
    "descascar_ps": "Descascar",
    "processo_umido": "Processo Úmido (PU)",
    "descascamento_pu": "Descascamento",
    "graos_pergaminho_umido": "Grãos de café em pergaminho úmido",
    "divisao_cereja": "Divisão da cereja",
    "remocao_agua": "Remoção de água",
    "secagem_pu": "Secagem",
    "lavagem_pu": "Lavagem",
    "graos_semisseco": "Grãos de café em pergaminho semisseco",
    "processo_mel": "Processo Mel (PM)",
    "secagem_pm": "Secagem",
    "gilin_basah": "Giling Basah",
    "casca_seca": "Casca seca",
    "graos_cafe_verde_pm": "Grãos de café verde"
}

def create_directories():
    """Cria a estrutura de diretórios do projeto Flask."""
    if not os.path.exists("templates"):
        os.makedirs("templates")
        print("Diretório 'templates' criado.")
    if not os.path.exists("static"):
        os.makedirs("static")
        print("Diretório 'static' criado.")

def create_app_file():
    """Cria o arquivo app.py com as rotas e a variável do diagrama."""
    app_content = """
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Variável do diagrama e base de conhecimento RAG ---
diagram_blocks = {
    "colheita": "Colheita",
    "classificacao": "Classificação",
    "cerejas_cafe": "Cerejas de café",
    "maceracao_carbonica": "Maceração Carbônica",
    "fermentacao_anaerobica": "Fermentação Anaeróbica",
    "digestao_animal": "Digestão Animal",
    "excrecao": "Excreção",
    "lavagem_digestao": "Lavagem",
    "descascamento_umido": "Descascamento Úmido",
    "secagem_umido": "Secagem",
    "graos_pergaminho_seco": "Grãos de café em pergaminho seco",
    "descascamento_seco": "Descascamento",
    "graos_cafe_verde": "Grãos de café verde",
    "fermentacao_microbiana": "Fermentação microbiana / enzimática",
    "secagem_final": "Secagem",
    "processo_seco": "Processo Seco (PS)",
    "cerejas_secas": "Cerejas Secas",
    "descascar_ps": "Descascar",
    "processo_umido": "Processo Úmido (PU)",
    "descascamento_pu": "Descascamento",
    "graos_pergaminho_umido": "Grãos de café em pergaminho úmido",
    "divisao_cereja": "Divisão da cereja",
    "remocao_agua": "Remoção de água",
    "secagem_pu": "Secagem",
    "lavagem_pu": "Lavagem",
    "graos_semisseco": "Grãos de café em pergaminho semisseco",
    "processo_mel": "Processo Mel (PM)",
    "secagem_pm": "Secagem",
    "gilin_basah": "Giling Basah",
    "casca_seca": "Casca seca",
    "graos_cafe_verde_pm": "Grãos de café verde"
}

knowledge_base = {
    "colheita": "A colheita do café pode ser manual (seletiva) ou mecânica...",
    "processo_seco": "O processo seco, também conhecido como 'natural', consiste em secar os frutos inteiros...",
    "fermentacao_anaerobica": "A fermentação anaeróbica ocorre na ausência de oxigênio...",
    "maceracao_carbonica": "A maceração carbônica é um processo de fermentação onde os grãos de café são colocados em um ambiente com dióxido de carbono...",
    "processo_mel": "O processo 'mel' ou 'honey' remove a casca do fruto, mas mantém o mucilago para a secagem...",
    "classificacao": "A classificação do café é feita após a colheita para separar os grãos por tamanho, densidade e qualidade...",
    "default": "Desculpe, não encontrei informações sobre este tópico na minha base de conhecimento."
}

def get_rag_response(query):
    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value
    return knowledge_base["default"]

@app.route('/')
def index():
    return render_template('index.html', title='Diagrama de Processamento de Grãos de Café', diagram_blocks=diagram_blocks)

# Rotas geradas automaticamente para cada bloco
"""
    for route_name, page_title in diagram_blocks.items():
        app_content += f"""
@app.route('/{route_name}')
def {route_name}():
    return render_template('{route_name}.html', title='{page_title}')
"""
    app_content += """
@app.route('/rag', methods=['POST'])
def rag_api():
    user_input = request.json.get('user_input', '')
    response = get_rag_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
"""
    with open("app.py", "w", encoding="utf-8") as f:
        f.write(app_content)
    print("Arquivo 'app.py' criado com sucesso.")


def create_base_template():
    """Cria o arquivo base.html com a interface do agente RAG integrada."""
    base_content = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="main-container">
        {% block content %}{% endblock %}
    </div>

    <div class="rag-interface">
        <button id="toggle-rag-button">Falar com o Agente RAG</button>
        <div id="rag-content" style="display: none;">
            <p>Faça uma pergunta sobre os processos do café:</p>
            <textarea id="user-input" rows="3" placeholder="Ex: O que é maceração carbônica?"></textarea>
            <button id="send-rag-button">Perguntar</button>
            <div id="rag-response-container">
                <p id="rag-response"></p>
            </div>
        </div>
    </div>

    <script>
        const toggleButton = document.getElementById('toggle-rag-button');
        const ragContent = document.getElementById('rag-content');
        const sendButton = document.getElementById('send-rag-button');
        const userInput = document.getElementById('user-input');
        const ragResponse = document.getElementById('rag-response');

        toggleButton.addEventListener('click', () => {
            ragContent.style.display = ragContent.style.display === 'none' ? 'block' : 'none';
        });

        sendButton.addEventListener('click', async () => {
            const query = userInput.value;
            if (!query) return;
            ragResponse.textContent = "Buscando resposta...";

            try {
                const response = await fetch('/rag', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ user_input: query })
                });
                const data = await response.json();
                ragResponse.textContent = data.response;
            } catch (error) {
                console.error('Erro:', error);
                ragResponse.textContent = 'Ocorreu um erro ao processar sua solicitação.';
            }
        });
    </script>
</body>
</html>
"""
    with open("templates/base.html", "w", encoding="utf-8") as f:
        f.write(base_content)
    print("Arquivo 'templates/base.html' criado com a interface RAG integrada.")

def create_diagram_page():
    """Cria o arquivo index.html usando a imagem e o mapa de imagem."""
    index_content = """
{% extends "base.html" %}

{% block title %}Diagrama de Processamento de Grãos de Café{% endblock %}

{% block content %}
    <div class="diagram-container">
        <h1>FIGURA 1: DIAGRAMA ESQUEMÁTICO DO PROCESSAMENTO DE GRÃOS DE CAFÉ</h1>
        <img src="{{ url_for('static', filename='diagrama.png') }}" alt="Diagrama de Processamento de Café" usemap="#diagrama-map" class="diagram-image">
        
        <map name="diagrama-map">
            {% for route_name, page_title in diagram_blocks.items() %}
            <area shape="rect" coords="0,0,0,0" href="{{ url_for(route_name) }}" alt="{{ page_title }}">
            {% endfor %}
            </map>
    </div>
{% endblock %}
"""
    with open("templates/index.html", "w", encoding="utf-8") as f:
        f.write(index_content)
    print("Arquivo 'templates/index.html' criado com a estrutura de mapa de imagem.")

def create_css_file():
    """Cria o arquivo style.css com estilos para a nova abordagem."""
    css_content = """
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f0f2f5;
}
.main-container {
    max-width: 1200px;
    margin: auto;
    padding: 20px;
}
.diagram-container {
    text-align: center;
    position: relative;
}
.diagram-image {
    max-width: 100%;
    height: auto;
}
.content-page {
    max-width: 800px;
    margin: 40px auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.rag-interface {
    position: fixed;
    bottom: 0;
    right: 20px;
    width: 300px;
    background-color: #f8f9fa;
    border: 1px solid #ccc;
    border-radius: 8px 8px 0 0;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    padding: 15px;
    box-sizing: border-box;
}
.rag-interface button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
}
.rag-interface button#toggle-rag-button {
    margin-bottom: 10px;
}
.rag-interface textarea {
    width: 100%;
    resize: none;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;
    margin-bottom: 10px;
}
.rag-interface #rag-response-container {
    margin-top: 10px;
    padding: 10px;
    background-color: #e9ecef;
    border-radius: 5px;
    min-height: 50px;
    font-size: 14px;
}
"""
    with open("static/style.css", "w", encoding="utf-8") as f:
        f.write(css_content)
    print("Arquivo 'static/style.css' criado com os novos estilos.")

def create_block_pages():
    """Cria os arquivos HTML para cada bloco do diagrama."""
    for route_name, page_title in diagram_blocks.items():
        content = f"""
{{% extends "base.html" %}}

{{% block title %}}{page_title}{{% endblock %}}

{{% block content %}}
    <div class="content-page">
        <h1>{page_title}</h1>
        <p>Esta é a página para o item '{page_title}'. Adicione aqui o conteúdo detalhado sobre este processo.</p>
        <p>A interface do Agente RAG está no canto inferior direito para você fazer perguntas a qualquer momento.</p>
    </div>
{{% endblock %}}
"""
        with open(f"templates/{route_name}.html", "w", encoding="utf-8") as f:
            f.write(content)
    print("Arquivos HTML para todos os blocos criados em 'templates/'.")


if __name__ == "__main__":
    create_directories()
    create_app_file()
    create_base_template()
    create_diagram_page()
    create_css_file()
    create_block_pages()
    print("\nProjeto gerado com sucesso! Próximos passos CRUCIAIS:")
    print("1. **Adicione a imagem do diagrama:** Coloque a imagem do seu diagrama em 'static/diagrama.png'.")
    print("2. **Edite 'templates/index.html':** Obtenha as coordenadas de cada quadro na imagem e preencha as tags <area>.")
    print("3. **Execute o servidor:** 'python app.py'")
    print("4. Acesse 'http://127.0.0.1:8000/' no seu navegador.")