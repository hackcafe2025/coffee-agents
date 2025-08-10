from flask import Flask, render_template_string

app = Flask(__name__)

# Dados dos blocos do diagrama com seus textos, cores e links (rotas)
blocks = [
    {"id": "colheita", "label": "Colheita", "color": "#d3d9f9", "top": 20, "left": 200},
    {"id": "classificacao", "label": "Classificação", "color": "#d3d9f9", "top": 70, "left": 200},
    {"id": "cerejas_cafe", "label": "Cerejas de café", "color": "#d3d9f9", "top": 120, "left": 200},
    {"id": "maceracao_carbonica", "label": "Maceração carbônica", "color": "#f5cccc", "top": 120, "left": 350},
    {"id": "digestao_animal", "label": "Digestão animal", "color": "#d9f2d9", "top": 80, "left": 600},
    {"id": "excrecao", "label": "Excreção", "color": "#d9f2d9", "top": 130, "left": 600},
    {"id": "lavagem", "label": "Lavagem", "color": "#d3d9f9", "top": 250, "left": 200},
    {"id": "fermentacao_anaerobica", "label": "Fermentação anaeróbica", "color": "#a1baff", "top": 150, "left": 100},
    {"id": "grãos_cafe_verde", "label": "Grãos de café verde", "color": "#d9f2d9", "top": 450, "left": 200}
]

@app.route("/")
def index():
    # Template HTML para o diagrama usando CSS inline para posicionamento dos blocos
    html = """
    <html>
    <head>
        <title>Diagrama de Processamento de Café</title>
        <style>
            body { font-family: Arial, sans-serif; }
            .diagram-container {
                position: relative;
                width: 800px;
                height: 600px;
                border: 1px solid #ccc;
                margin: 20px auto;
                background: #fdfdfd;
            }
            .block {
                position: absolute;
                padding: 10px 15px;
                border-radius: 5px;
                border: 1px solid #333;
                cursor: pointer;
                text-align: center;
                font-weight: bold;
                transition: background-color 0.3s ease;
                width: 150px;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            }
            .block:hover {
                background-color: #f0f0f0;
            }
            a {
                color: inherit;
                text-decoration: none;
                display: block;
            }
        </style>
    </head>
    <body>
        <h1 style="text-align:center;">Diagrama de Processamento de Grãos de Café</h1>
        <div class="diagram-container">
            {% for block in blocks %}
                <div class="block" style="top:{{block.top}}px; left:{{block.left}}px; background-color:{{block.color}};">
                    <a href="/agent/{{block.id}}">{{ block.label }}</a>
                </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html, blocks=blocks)


@app.route("/agent/<block_id>")
def agent_page(block_id):
    # Apenas uma página simples indicando qual agente foi acessado
    # Aqui você pode expandir para lógica do agente
    agent_labels = {b["id"]: b["label"] for b in blocks}
    label = agent_labels.get(block_id, "Agente Desconhecido")
    return f"""
    <html>
    <head><title>{label}</title></head>
    <body>
        <h1>Agente: {label}</h1>
        <p>Esta página representa o agente para o bloco "{label}".</p>
        <p><a href="/">Voltar para o diagrama</a></p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
