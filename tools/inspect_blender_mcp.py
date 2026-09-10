"""Read the running Blender MCP add-on without changing its scene or settings."""

import argparse
import json
import socket


def inspect(command="get_scene_info", port=9876):
    if command not in {"ping", "get_scene_info", "get_addon_info"}:
        raise ValueError("Only read-only inspection commands are supported")
    with socket.create_connection(("127.0.0.1", port), timeout=10) as connection:
        connection.settimeout(20)
        connection.sendall(json.dumps({"type": command, "params": {}}).encode("utf-8"))
        response = bytearray()
        while len(response) < 4 * 1024 * 1024:
            chunk = connection.recv(8192)
            if not chunk:
                break
            response.extend(chunk)
            try:
                return json.loads(response.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
        raise RuntimeError("Blender MCP returned an incomplete or oversized response")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--command", choices=("ping", "get_scene_info", "get_addon_info"), default="get_scene_info")
    parser.add_argument("--port", type=int, default=9876)
    arguments = parser.parse_args()
    print(json.dumps(inspect(arguments.command, arguments.port), ensure_ascii=False, indent=2))
