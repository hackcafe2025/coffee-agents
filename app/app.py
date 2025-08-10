# Flask API simples que expõe endpoints para análise e execução de ações
from flask import Flask, request, jsonify
from agents import Orchestrator
import os

app = Flask(__name__)
orch = Orchestrator()

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json() or {}
    topic = data.get("topic", "fermentação anaeróbica")
    try:
        result = orch.run_analysis(topic)
        return jsonify({"status": "ok", "result": result})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route("/api/start_drying", methods=["POST"])
def start_drying():
    data = request.get_json() or {}
    job_id = data.get("job_id", "job-auto-1")
    temp = float(data.get("temp", 35.0))
    try:
        res = orch.run_action_start_drying(job_id, temp)
        return jsonify({"status": "ok", "mcp_result": res})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route("/")
def index():
    return "<h3>Coffee-Agents API</h3><p>POST /api/analyze and /api/start_drying</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
