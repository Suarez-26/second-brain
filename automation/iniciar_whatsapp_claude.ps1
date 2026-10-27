$ErrorActionPreference = "Stop"
$Raiz = Split-Path -Parent $PSScriptRoot
$BridgeDir = Join-Path $PSScriptRoot "whatsapp-mcp\whatsapp-bridge-node"
$BotScript = Join-Path $PSScriptRoot "claude_whatsapp_bot.py"
$PythonExe = "C:\Users\tomas\AppData\Local\Python\pythoncore-3.14-64\python.exe"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Iniciando Sistema Interactivo Claude + WhatsApp (Pao)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Verificar si el Bridge ya está escuchando en 127.0.0.1:8085
$bridgeRunning = $false
try {
    $resp = Invoke-RestMethod -Uri "http://127.0.0.1:8085/api/status" -TimeoutSec 2
    $bridgeRunning = $true
    Write-Host "[OK] WhatsApp Bridge ya está activo en http://127.0.0.1:8085" -ForegroundColor Green
} catch {
    Write-Host "[1/2] Iniciando WhatsApp Bridge (Node.js) en puerto 8085..." -ForegroundColor Yellow
    Start-Process -FilePath "node" -ArgumentList "index.js" -WorkingDirectory $BridgeDir -WindowStyle Normal
    Start-Sleep -Seconds 3
}

# 2. Abrir página QR si aún no está vinculado
try {
    $status = Invoke-RestMethod -Uri "http://127.0.0.1:8085/api/status" -TimeoutSec 3
    if (-not $status.connected) {
        Write-Host "📲 Abriendo http://127.0.0.1:8085/qr en el navegador para escanear el código QR..." -ForegroundColor Magenta
        Start-Process "http://127.0.0.1:8085/qr"
    } else {
        Write-Host "✓ WhatsApp conectado como: $($status.my_jid)" -ForegroundColor Green
    }
} catch {}

# 3. Iniciar el Bot Interactivo de Claude
Write-Host "[2/2] Iniciando Bot Interactivo de Claude (claude_whatsapp_bot.py)..." -ForegroundColor Yellow
& $PythonExe $BotScript
