# cliente HTTP simples para o MCP stub
import requests
from config import MCP_SERVER_URL

class MCPClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or MCP_SERVER_URL.rstrip('/')

    def call_tool(self, tool_name: str, payload: dict):
        url = f"{self.base_url}/{tool_name}"
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
        return resp.json().get("result")

# helper singleton
mcp_client = MCPClient()