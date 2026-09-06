$ErrorActionPreference = 'Stop'
$frutiRoot = Split-Path -Parent $PSScriptRoot
$frutiPython = Join-Path $frutiRoot '.tools/unity-mcp-venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $frutiPython)) { throw 'Falta el entorno local de MCP. Consulta docs/UNITY_MCP.md.' }
try {
    $frutiHealth = Invoke-WebRequest 'http://127.0.0.1:8080/health' -UseBasicParsing -TimeoutSec 2
    if ($frutiHealth.StatusCode -eq 200) { Write-Output 'MCP ya está activo en 127.0.0.1:8080'; exit 0 }
} catch { }
New-Item -ItemType Directory -Force -Path (Join-Path $frutiRoot 'artifacts') | Out-Null
$env:UNITY_MCP_DISABLE_TELEMETRY = 'true'
$frutiProcess = Start-Process -FilePath $frutiPython -ArgumentList '-m main --transport http --http-url http://127.0.0.1:8080' -WorkingDirectory $frutiRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $frutiRoot 'artifacts/unity-mcp-server.out.log') -RedirectStandardError (Join-Path $frutiRoot 'artifacts/unity-mcp-server.err.log') -PassThru
Write-Output "MCP iniciado: PID $($frutiProcess.Id), http://127.0.0.1:8080/mcp"
