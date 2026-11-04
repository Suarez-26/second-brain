# Iniciar Kapso WhatsApp Bot + Cloudflare Tunnel
$ErrorActionPreference = "Continue"

$Raiz = Split-Path -Parent $PSScriptRoot
$PythonExe = if ($env:SECOND_BRAIN_PYTHON) { $env:SECOND_BRAIN_PYTHON } else { (Get-Command python -ErrorAction SilentlyContinue).Source }
$CloudflaredExe = Join-Path $PSScriptRoot "cloudflared.exe"
$BotScript = Join-Path $PSScriptRoot "kapso_whatsapp_bot.py"
$LogCloudflared = Join-Path $PSScriptRoot "cloudflared.log"
$EnvFile = Join-Path $Raiz ".env"
$SkillsDir = Join-Path $Raiz ".agents\skills\integrate-whatsapp\scripts"
$SecretosDir = Join-Path $PSScriptRoot ".secretos"

if (-not $PythonExe) { Write-Host "ERROR: no encuentro python en el PATH (o define SECOND_BRAIN_PYTHON)." -ForegroundColor Red; exit 1 }
if (-not (Test-Path $CloudflaredExe)) { Write-Host "ERROR: falta automation\cloudflared.exe" -ForegroundColor Red; exit 1 }

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Servidor Kapso WhatsApp Bot + Second Brain" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Limpiar procesos previos
Get-Process -Name "cloudflared" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }

# 2. Iniciar Cloudflare Tunnel hacia el puerto 5000
Write-Host "1/3: Levantando tunel Cloudflare..." -ForegroundColor Yellow
if (Test-Path $LogCloudflared) { Remove-Item $LogCloudflared -Force }
$procTunnel = Start-Process -FilePath $CloudflaredExe -ArgumentList "tunnel --url http://127.0.0.1:5000 --logfile `"$LogCloudflared`"" -PassThru -WindowStyle Hidden

# 3. Obtener URL publica de trycloudflare.com
$publicUrl = ""
Write-Host "2/3: Esperando URL publica de trycloudflare.com..." -ForegroundColor Yellow
for ($i = 0; $i -lt 45; $i++) {
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
    Write-Host "ERROR: No se pudo obtener la URL de Cloudflare Tunnel. Revisa $LogCloudflared" -ForegroundColor Red
    if ($procTunnel -and -not $procTunnel.HasExited) { $procTunnel.Kill() }
    exit 1
}
$webhookUrl = "$publicUrl/webhook"
Write-Host "OK: Endpoint webhook: $webhookUrl" -ForegroundColor Green

# 4. Recrear webhooks en Kapso. El secreto de firma de cada uno queda en automation\.secretos\ (ignorado por git)
Write-Host "3/3: Sincronizando webhooks en Kapso..." -ForegroundColor Yellow
$targetPhones = if ($env:KAPSO_PHONE_NUMBER_IDS) { $env:KAPSO_PHONE_NUMBER_IDS -split "," } else { @("597907523413541") }

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
} catch { Write-Host "WARN: no se pudieron listar los webhooks anteriores: $_" -ForegroundColor Yellow }

# Los secretos viejos ya no sirven: sus webhooks se borraron arriba
if (Test-Path $SecretosDir) { Get-ChildItem -Path $SecretosDir -Filter "*.json" | Remove-Item -Force }
New-Item -ItemType Directory -Force $SecretosDir | Out-Null

$conectados = 0
foreach ($phoneId in $targetPhones) {   # ojo: $pid es variable reservada de PowerShell
    try {
        $env:KAPSO_SECRET_OUTPUT_FILE = Join-Path $SecretosDir "webhook_$phoneId.json"
        $createOut = & node --env-file="$EnvFile" "$SkillsDir\create.js" --scope project --url "$webhookUrl" --events whatsapp.message.received --phone-number-id $phoneId
        $parsedCreate = $createOut | ConvertFrom-Json
        if ($parsedCreate.ok) {
            Write-Host "OK: Webhook conectado para Phone ID $phoneId" -ForegroundColor Green
            $conectados++
        } else {
            Write-Host "WARN: Kapso rechazo el webhook para $phoneId. Revisa app.kapso.ai" -ForegroundColor Yellow
        }
    } catch { Write-Host "WARN: error creando webhook para ${phoneId}: $_" -ForegroundColor Yellow }
    finally { Remove-Item Env:\KAPSO_SECRET_OUTPUT_FILE -ErrorAction SilentlyContinue }
}
if ($conectados -eq 0) { Write-Host "WARN: ningun webhook quedo conectado; el bot no recibira mensajes." -ForegroundColor Yellow }

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " BOT ACTIVO. Terceros -> borradores en copiloto; open-loops -> propuestas." -ForegroundColor Green
Write-Host " (Ctrl+C para detener)" -ForegroundColor DarkGray
Write-Host "==========================================================" -ForegroundColor Cyan

# 5. Ejecutar el servidor Python en primer plano
try {
    & $PythonExe $BotScript
} finally {
    Write-Host "`nDeteniendo tunel Cloudflare..." -ForegroundColor Yellow
    if ($procTunnel -and -not $procTunnel.HasExited) { $procTunnel.Kill() }
}
