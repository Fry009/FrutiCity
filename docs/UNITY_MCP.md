# Unity MCP en FrutiCity

Puente instalado: [CoplayDev MCP for Unity](https://github.com/CoplayDev/unity-mcp), versión 10.2.0, commit `30d22075093d1d35dfb0091c1c7550e9ad948577`.

- Paquete del editor: `FrutiCity/Packages/manifest.json`, fijado al commit.
- Servidor Python local: `.tools/unity-mcp-venv/` (ignorado en git).
- Transporte: HTTP en `http://127.0.0.1:8080/mcp`, solo loopback.
- Codex: servidor `unity` registrado en la configuración personal mediante `codex mcp add unity --url http://127.0.0.1:8080/mcp`.
- Arranque: el editor ejecuta `tools/Start-UnityMcp.ps1` y conecta el puente al cargar. Las validaciones batch no lo arrancan.
- Reintento manual: **FrutiCity > MCP > Connect local Unity MCP**.
- Registros: `artifacts/unity-mcp-server.err.log` y `artifacts/unity-mcp-server.out.log`.

Los cambios de herramientas pueden requerir una nueva sesión de Codex. Durante la instalación se puede usar el cliente CLI del mismo puente para comprobar la conexión real:

```powershell
$env:PYTHONIOENCODING='utf-8'
.tools/unity-mcp-venv/Scripts/unity-mcp.exe -f json instances
.tools/unity-mcp-venv/Scripts/unity-mcp.exe -f json scene hierarchy
```

Para reconstruir el entorno en otra máquina, desde la raíz del repositorio:

```powershell
git clone --depth 1 --branch v10.2.0 https://github.com/CoplayDev/unity-mcp.git .tools/unity-mcp
uv venv .tools/unity-mcp-venv
uv pip install --python .tools/unity-mcp-venv/Scripts/python.exe .tools/unity-mcp/Server
powershell -ExecutionPolicy Bypass -File tools/Start-UnityMcp.ps1
```

Telemetría desactivada en el servidor y en las preferencias del puente. El paquete solo interviene en el editor; no es una dependencia del juego publicado.

Configuración de Codex basada en su [documentación MCP](https://developers.openai.com/codex/mcp/).

## Comprobación realizada el 6 de septiembre de 2026

Servidor y editor conectados: proyecto `FrutiCity`, hash `f7d925741fd94b2a`, Unity `6000.6.0f1`. Se han ejecutado mediante el cliente MCP del puente:

- Lectura de jerarquía: escena FrutiCity, cámara y componente FrutiCityApp.
- Entrada en Play.
- Apertura de Casa, Fusionar, Jugar, Personajes, Historia y Tienda con controles activos.
- Comprobación de la ficha de Mona y avance del diálogo con el botón Seguir.
- Regreso a Casa y lectura de consola: cero errores actuales.

Los scripts de comprobación quedan en `artifacts/mcp-ui-check.cs` y `artifacts/mcp-navigation-check.cs`.
