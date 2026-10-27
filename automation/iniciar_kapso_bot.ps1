# Iniciar Kapso WhatsApp Bot + Cloudflare Tunnel
$ErrorActionPreference = "Continue"

$Raiz = Split-Path -Parent $PSScriptRoot
$PythonExe = "C:\Users\tomas\AppData\Local\Python\pythoncore-3.14-64\python.exe"
$CloudflaredExe = Join-Path $PSScriptRoot "cloudflared.exe"
$BotScript = Join-Path $PSScriptRoot "kapso_whatsapp_bot.py"
$LogCloudflared = Join-Path $PSScriptRoot "cloudflared.log"
$EnvFile = Join-Path $Raiz ".env"
$SkillsDir = Join-Path $Raiz ".agents\skills\integrate-whatsapp\scripts"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Servidor Kapso WhatsApp Bot + Second Brain" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Limpiar procesos previos
Get-Process -Name "cloudflared" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }

# 2. Iniciar Cloudflare Tunnel hacia el puerto 5000
Write-Host "1/3: Levantando tunel Cloudflare seguro..." -ForegroundColor Yellow
if (Test-Path $LogCloudflared) { Remove-Item $LogCloudflared -Force }

$procTunnel = Start-Process -FilePath $CloudflaredExe -ArgumentList "tunnel --url http://127.0.0.1:5000 --logfile `"$LogCloudflared`"" -PassThru -WindowStyle Hidden

# 3. Obtener URL publica de trycloudflare.com
$publicUrl = ""
Write-Host "2/3: Esperando URL publica de trycloudflare.com..." -ForegroundColor Yellow
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 1
    if (Test-Path $LogCloudflared) {
        $contenido = Get-Content $LogCloudflared -Raw -ErrorAction SilentlyContinue
        if ($contenido -match "https://[a-zA-Z0-9-]+\.trycloudflare\.com") {
            $publicUrl = $matches[0]
            break
        }
    }
}

if (-not $publicUrl) {
    Write-Host "ERROR: No se pudo obtener la URL de Cloudflare Tunnel." -ForegroundColor Red
    if ($procTunnel -and -not $procTunnel.HasExited) { $procTunnel.Kill() }
    exit 1
}

$webhookUrl = "$publicUrl/webhook"
Write-Host "OK: Tunel publico: $publicUrl" -ForegroundColor Green
Write-Host "OK: Endpoint webhook: $webhookUrl" -ForegroundColor Green

# 4. Sincronizar Webhook en Kapso con las skills oficiales
Write-Host "3/3: Sincronizando Webhooks en Kapso (Sandbox y Produccion)..." -ForegroundColor Yellow

$targetPhones = @("597907523413541", "1455485914304122")

# Limpiar webhooks anteriores para estos numeros
try {
    $listJson = & node --env-file="$EnvFile" "$SkillsDir\list.js" --scope project
    $parsedList = $listJson | ConvertFrom-Json
    if ($parsedList.ok -and $parsedList.data.data) {
        foreach ($wh in $parsedList.data.data) {
            if ($targetPhones -contains $wh.phone_number_id) {
                & node --env-file="$EnvFile" "$SkillsDir\delete.js" --scope project --webhook-id $wh.id | Out-Null
            }
        }
    }
} catch {}

# Crear nuevos webhooks
foreach ($pid in $targetPhones) {
    try {
        $createOut = & node --env-file="$EnvFile" "$SkillsDir\create.js" --scope project --url "$webhookUrl" --events whatsapp.message.received --phone-number-id $pid
        $parsedCreate = $createOut | ConvertFrom-Json
        if ($parsedCreate.ok) {
            Write-Host "OK: Webhook conectado para Phone ID $pid!" -ForegroundColor Green
        } else {
            Write-Host "WARN: Verifique registro en app.kapso.ai para $pid" -ForegroundColor Yellow
        }
    } catch {}
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " BOT WHATSAPP + SECOND BRAIN ACTIVO Y LISTO" -ForegroundColor Green
Write-Host "  Numero WhatsApp: +1 555-329-9391" -ForegroundColor Cyan
Write-Host "  Audios: Transcribe y guarda en journal/ con faster-whisper" -ForegroundColor Cyan
Write-Host "  Notas: Lee y edita Second Brain en tiempo real" -ForegroundColor Cyan
Write-Host "  (Presiona Ctrl+C en cualquier momento para detener)" -ForegroundColor DarkGray
Write-Host "==========================================================" -ForegroundColor Cyan

# 5. Ejecutar el servidor Python en primer plano
try {
    & $PythonExe $BotScript
} finally {
    Write-Host "`nDeteniendo tunel Cloudflare..." -ForegroundColor Yellow
    if ($procTunnel -and -not $procTunnel.HasExited) {
        $procTunnel.Kill()
    }
    Write-Host "Bot detenido correctamente." -ForegroundColor Green
}
