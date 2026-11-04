# Programar Tarea Diaria en Windows (Task Scheduler) para Investigar a Diego Tarazona a las 06:00 AM
$ErrorActionPreference = "Stop"

$Raiz = Split-Path -Parent $PSScriptRoot
$BatPath = Join-Path $PSScriptRoot "ejecutar_investigacion_diego.bat"
$TaskName = "SecondBrain_Investigacion_Diego_Tarazona"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Programando Tarea Diaria en Windows: $TaskName" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

if (-not (Test-Path $BatPath)) {
    Write-Host "ERROR: No existe $BatPath" -ForegroundColor Red
    exit 1
}

# Crear acción y disparador a las 6:00 AM
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$BatPath`"" -WorkingDirectory $Raiz
$trigger = New-ScheduledTaskTrigger -Daily -At 6:00am
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

try {
    # Eliminar si ya existía previamente
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    
    # Registrar tarea para el usuario actual
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Description "Extracción e investigación diaria sobre Diego Tarazona y Campuslands para el Second Brain" -User $env:USERNAME
    
    Write-Host "`n[OK] Tarea programada exitosamente." -ForegroundColor Green
    Write-Host "  - Nombre: $TaskName" -ForegroundColor Yellow
    Write-Host "  - Frecuencia: Todos los días a las 06:00 AM" -ForegroundColor Yellow
    Write-Host "  - Acción: $BatPath" -ForegroundColor Yellow
} catch {
    Write-Host "`n[ERROR] al registrar la tarea: $_" -ForegroundColor Red
    Write-Host "Intenta ejecutar PowerShell como Administrador si se requieren privilegios elevados." -ForegroundColor DarkYellow
}
