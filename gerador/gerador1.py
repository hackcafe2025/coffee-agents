import os

# Lista de todos os blocos/quadros do diagrama
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

agent_interface_html_content = """
{% extends "base.html" %}

{% block title %}Agente de Café RAG{% endblock %}

{% block content %}
    <div class="agent-container">
        <h1>Agente de Informação sobre Café</h1>
        <p>Faça uma pergunta sobre os processos do café, por exemplo: "O que é o processo seco?".</p>
        <form id="agent-form">
            <input type="text" id="user-input" name="user_input" placeholder="Digite sua pergunta aqui..." required>
            <button type="submit">Perguntar</button>
        </form>
        <div id="response-container">
            <p id="agent-response"></p>
        </div>
    </div>

    <script>
        const form = document.getElementById('agent-form');
        const userInput = document.getElementById('user-input');
        const agentResponse = document.getElementById('agent-response');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const query = userInput.value;
            agentResponse.textContent = "Buscando resposta...";

            try {
                const response = await fetch('/agente', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ user_input: query })
                });
                const data = await response.json();
                agentResponse.textContent = data.response;
            } catch (error) {
                console.error('Erro:', error);
                agentResponse.textContent = 'Ocorreu um erro ao processar sua solicitação.';
            }
        });
    </script>
    <style>
        .agent-container {
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        #agent-form {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        #user-input {
            flex-grow: 1;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        #response-container {
            padding: 15px;
            background-color: #f9f9f9;
            border: 1px solid #eee;
            border-radius: 5px;
        }
    </style>
{% endblock %}
"""

def create_directories():
    """Cria a estrutura de diretórios do projeto Flask."""
    if not os.path.exists("templates"):
        os.makedirs("templates")
        print("Diretório 'templates' criado.")
    if not os.path.exists("static"):
        os.makedirs("static")
        print("Diretório 'static' criado.")

def create_app_file():
    """Cria o arquivo app.py com as rotas."""
    app_content = """
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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
    return render_template('index.html')

# Rotas geradas automaticamente
"""
    for route_name, page_title in diagram_blocks.items():
        app_content += f"""
@app.route('/{route_name}')
def {route_name}():
    return render_template('{route_name}.html', title='{page_title}')
"""
    app_content += """
@app.route('/agente', methods=['GET', 'POST'])
def agente():
    if request.method == 'POST':
        user_input = request.json.get('user_input', '')
        response = get_rag_response(user_input)
        return jsonify({'response': response})
    return render_template('agent_interface.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
"""
    with open("app.py", "w", encoding="utf-8") as f:
        f.write(app_content)
    print("Arquivo 'app.py' criado com sucesso.")


def create_base_template():
    """Cria o arquivo base.html."""
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
    <div class="footer">
        <a href="{{ url_for('index') }}">Voltar ao Diagrama</a> |
        <a href="{{ url_for('agente') }}">Falar com o Agente RAG</a>
    </div>
</body>
</html>
"""
    with open("templates/base.html", "w", encoding="utf-8") as f:
        f.write(base_content)
    print("Arquivo 'templates/base.html' criado.")


def create_diagram_page():
    """Cria o arquivo index.html com o esqueleto do diagrama."""
    index_content = """
{% extends "base.html" %}

{% block title %}Diagrama de Processamento de Grãos de Café{% endblock %}

{% block content %}
    <div class="diagram-container">
        <h2 class="diagram-title">FIGURA 1: DIAGRAMA ESQUEMÁTICO DO PROCESSAMENTO DE GRÃOS DE CAFÉ ATUAL E EMERGENTE, ADAPTADO DE FEBRIANTO E ZHU (2023)</h2>
"""
    for route_name, page_title in diagram_blocks.items():
        index_content += f"""
        <a href="{{{{ url_for('{route_name}') }}}}" class="block {route_name}">{page_title}</a>
"""

    index_content += """
    </div>
{% endblock %}
"""

    with open("templates/index.html", "w", encoding="utf-8") as f:
        f.write(index_content)
    print("Arquivo 'templates/index.html' criado com links para todos os blocos.")


def create_css_file():
    """Cria o arquivo style.css com estilos básicos."""
    css_content = """
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f0f2f5;
}

.main-container {
    padding-bottom: 60px;
}

.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    background-color: #333;
    color: white;
    text-align: center;
    padding: 10px;
    box-sizing: border-box;
}

.footer a {
    color: white;
    text-decoration: none;
    margin: 0 15px;
}

.footer a:hover {
    text-decoration: underline;
}

.diagram-container {
    position: relative;
    width: 1200px;
    height: 1200px;
    margin: 40px auto;
    background-color: #ffffff;
    border: 1px solid #ccc;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    padding: 20px;
}

.diagram-title {
    text-align: center;
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 30px;
}

.block {
    position: absolute;
    padding: 10px 15px;
    border: 1px solid #000;
    background-color: #f8f8f8;
    text-align: center;
    font-size: 12px;
    min-width: 150px;
    box-sizing: border-box;
    border-radius: 5px;
    text-decoration: none;
    color: #333;
    transition: all 0.3s ease;
}

.block:hover {
    background-color: #e0e0e0;
    box-shadow: 0 0 5px rgba(0,0,0,0.2);
}

/* ---------------------------------------------------- */
/* POSICIONAMENTO DOS QUADROS (AJUSTE!)       */
/* ---------------------------------------------------- */
.colheita { top: 20px; left: 450px; }
.classificacao { top: 80px; left: 450px; }
.cerejas_cafe { top: 140px; left: 450px; }
.descascamento_pu { top: 200px; left: 450px; }
.graos_pergaminho_umido { top: 260px; left: 450px; }
.divisao_cereja { top: 320px; left: 450px; }
.lavagem_pu { top: 380px; left: 450px; }
.secagem_pu { top: 440px; left: 450px; }
.graos_semisseco { top: 500px; left: 450px; }
.processo_seco { top: 380px; left: 150px; }
.cerejas_secas { top: 440px; left: 150px; }
.descascar_ps { top: 500px; left: 150px; }
.graos_cafe_verde { top: 560px; left: 150px; }
.processo_mel { top: 200px; left: 750px; }
.secagem_pm { top: 260px; left: 750px; }
.maceracao_carbonica { top: 140px; left: 750px; background-color: #f8cbad; }
.fermentacao_anaerobica { top: 260px; left: 150px; background-color: #d1c7f1; }
.digestao_animal { top: 20px; left: 750px; background-color: #c7f1c7; }
/* ...adicione os demais quadros aqui... */
"""
    with open("static/style.css", "w", encoding="utf-8") as f:
        f.write(css_content)
    print("Arquivo 'static/style.css' criado.")

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
        <p>Você pode usar a interface do agente RAG para obter mais informações sobre este ou outros tópicos.</p>
    </div>
    <style>
        .content-page {{
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
    </style>
{{% endblock %}}
"""
        with open(f"templates/{route_name}.html", "w", encoding="utf-8") as f:
            f.write(content)
    print("Arquivos HTML para todos os blocos criados em 'templates/'.")


def create_agent_page():
    """Cria a página da interface do agente."""
    with open("templates/agent_interface.html", "w", encoding="utf-8") as f:
        f.write(agent_interface_html_content)
    print("Arquivo 'templates/agent_interface.html' criado.")

if __name__ == "__main__":
    create_directories()
    create_app_file()
    create_base_template()
    create_diagram_page()
    create_css_file()
    create_block_pages()
    create_agent_page()
    print("\nProjeto gerado com sucesso! Agora, por favor:")
    print("1. Instale o Flask: 'pip install Flask'")
    print("2. Execute o servidor: 'python app.py'")
    print("3. Acesse 'http://127.0.0.1:8000/' no seu navegador (porta 8000).")
    print("4. **Importante:** Edite 'static/style.css' para ajustar o posicionamento dos quadros.")