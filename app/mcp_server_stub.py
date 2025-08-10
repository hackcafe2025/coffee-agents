# Exemplo mínimo de MCP server stub (conceitual).
# Use o SDK real do Model Context Protocol que você escolher.

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse as urlparse

HOST = "0.0.0.0"
PORT = 8001

# Ferramentas simuladas
def start_drying(payload):
    job_id = payload.get("job_id", "job-123")
    temp = payload.get("temp", 35.0)
    return {"status": "started", "job_id": job_id, "temp": temp}

def fetch_process_notes(payload):
    topic = payload.get("topic", "geral")
    return {"topic": topic, "notes": f"Notas sinteticas sobre {topic} - (stub MCP)"}

TOOLS = {
    "start_drying": start_drying,
    "fetch_notes": fetch_process_notes
}

class SimpleHandler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        self.send_response(code)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body).encode('utf-8'))

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw) if raw else {}
        except:
            payload = {}
        path = urlparse.urlparse(self.path).path.strip("/")
        tool = path
        if tool in TOOLS:
            res = TOOLS[tool](payload)
            self._send(200, {"result": res})
        else:
            self._send(404, {"error": "tool not found", "available": list(TOOLS.keys())})

if __name__ == "__main__":
    print(f"MCP stub server listening on {HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), SimpleHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()