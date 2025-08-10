
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

@app.route('/colheita')
def colheita():
    return render_template('colheita.html', title='Colheita')

@app.route('/classificacao')
def classificacao():
    return render_template('classificacao.html', title='Classificação')

@app.route('/cerejas_cafe')
def cerejas_cafe():
    return render_template('cerejas_cafe.html', title='Cerejas de café')

@app.route('/maceracao_carbonica')
def maceracao_carbonica():
    return render_template('maceracao_carbonica.html', title='Maceração Carbônica')

@app.route('/fermentacao_anaerobica')
def fermentacao_anaerobica():
    return render_template('fermentacao_anaerobica.html', title='Fermentação Anaeróbica')

@app.route('/digestao_animal')
def digestao_animal():
    return render_template('digestao_animal.html', title='Digestão Animal')

@app.route('/excrecao')
def excrecao():
    return render_template('excrecao.html', title='Excreção')

@app.route('/lavagem_digestao')
def lavagem_digestao():
    return render_template('lavagem_digestao.html', title='Lavagem')

@app.route('/descascamento_umido')
def descascamento_umido():
    return render_template('descascamento_umido.html', title='Descascamento Úmido')

@app.route('/secagem_umido')
def secagem_umido():
    return render_template('secagem_umido.html', title='Secagem')

@app.route('/graos_pergaminho_seco')
def graos_pergaminho_seco():
    return render_template('graos_pergaminho_seco.html', title='Grãos de café em pergaminho seco')

@app.route('/descascamento_seco')
def descascamento_seco():
    return render_template('descascamento_seco.html', title='Descascamento')

@app.route('/graos_cafe_verde')
def graos_cafe_verde():
    return render_template('graos_cafe_verde.html', title='Grãos de café verde')

@app.route('/fermentacao_microbiana')
def fermentacao_microbiana():
    return render_template('fermentacao_microbiana.html', title='Fermentação microbiana / enzimática')

@app.route('/secagem_final')
def secagem_final():
    return render_template('secagem_final.html', title='Secagem')

@app.route('/processo_seco')
def processo_seco():
    return render_template('processo_seco.html', title='Processo Seco (PS)')

@app.route('/cerejas_secas')
def cerejas_secas():
    return render_template('cerejas_secas.html', title='Cerejas Secas')

@app.route('/descascar_ps')
def descascar_ps():
    return render_template('descascar_ps.html', title='Descascar')

@app.route('/processo_umido')
def processo_umido():
    return render_template('processo_umido.html', title='Processo Úmido (PU)')

@app.route('/descascamento_pu')
def descascamento_pu():
    return render_template('descascamento_pu.html', title='Descascamento')

@app.route('/graos_pergaminho_umido')
def graos_pergaminho_umido():
    return render_template('graos_pergaminho_umido.html', title='Grãos de café em pergaminho úmido')

@app.route('/divisao_cereja')
def divisao_cereja():
    return render_template('divisao_cereja.html', title='Divisão da cereja')

@app.route('/remocao_agua')
def remocao_agua():
    return render_template('remocao_agua.html', title='Remoção de água')

@app.route('/secagem_pu')
def secagem_pu():
    return render_template('secagem_pu.html', title='Secagem')

@app.route('/lavagem_pu')
def lavagem_pu():
    return render_template('lavagem_pu.html', title='Lavagem')

@app.route('/graos_semisseco')
def graos_semisseco():
    return render_template('graos_semisseco.html', title='Grãos de café em pergaminho semisseco')

@app.route('/processo_mel')
def processo_mel():
    return render_template('processo_mel.html', title='Processo Mel (PM)')

@app.route('/secagem_pm')
def secagem_pm():
    return render_template('secagem_pm.html', title='Secagem')

@app.route('/gilin_basah')
def gilin_basah():
    return render_template('gilin_basah.html', title='Giling Basah')

@app.route('/casca_seca')
def casca_seca():
    return render_template('casca_seca.html', title='Casca seca')

@app.route('/graos_cafe_verde_pm')
def graos_cafe_verde_pm():
    return render_template('graos_cafe_verde_pm.html', title='Grãos de café verde')

@app.route('/rag', methods=['POST'])
def rag_api():
    user_input = request.json.get('user_input', '')
    response = get_rag_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
