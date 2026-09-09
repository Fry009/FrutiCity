"""Cliente del MCP de Blender (protocolo socket TCP JSON del addon).

Uso:
    python blender_mcp_client.py get_addon_info
    python blender_mcp_client.py get_scene_info
    python blender_mcp_client.py execute_code "{...codigo...}"
    python blender_mcp_client.py get_viewport_screenshot "{...params...}"

El puerto se lee de BLENDER_MCP_PORT (default 9191). Devuelve la respuesta
cruda del addon por stdout; los errores de red van a stderr.
"""
import json
import os
import socket
import sys
import time

HOST = os.environ.get("BLENDER_MCP_HOST", "127.0.0.1")
PORT = int(os.environ.get("BLENDER_MCP_PORT", "9191"))
BUFSIZE = 65536


def send_command(cmd_type, params=None, timeout=120):
    """Envia un comando JSON y lee la respuesta JSON completa."""
    payload = json.dumps({"type": cmd_type, "params": params or {}})

    client = socket.create_connection((HOST, PORT), timeout=15)
    client.settimeout(timeout)
    client.sendall(payload.encode("utf-8"))

    buffer = b""
    deleted_lines = 0
    while True:
        try:
            data = client.recv(BUFSIZE)
        except socket.timeout:
            client.close()
            raise TimeoutError(
                f"Blender no respondio en {timeout}s a '{cmd_type}' "
                f"(buffer: {len(buffer)} bytes)"
            )
        if not data:
            client.close()
            if not buffer:
                raise ConnectionError("Blender cerro la conexion sin responder")
            break
        buffer += data
        try:
            response = json.loads(buffer.decode("utf-8"))
            client.close()
            return response
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2

    cmd_type = sys.argv[1]
    params = {}
    if len(sys.argv) > 2:
        raw = sys.argv[2]
        if raw.startswith("@"):
            import os
            p = os.path.join(os.path.dirname(os.path.abspath(__file__)), raw[1:])
            with open(p, encoding="utf-8-sig") as f:
                params = json.load(f)
        elif raw.strip().startswith("{"):
            params = json.loads(raw)
        else:
            params = {"text": raw}

    try:
        response = send_command(cmd_type, params)
    except (ConnectionError, TimeoutError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(json.dumps(response, ensure_ascii=False, indent=2))
    if response.get("status") == "error":
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())