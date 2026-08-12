#Requires -Version 5.1
<#
.SYNOPSIS
    Installs dependencies into an isolated venv and starts the EYRIC RYTHOS AI API.

.DESCRIPTION
    Creates .venv (isolated from the machine-wide Python so dependency pins are
    honoured), installs requirements.txt, bootstraps .env, then serves the
    FastAPI app defined in app/main.py.

.PARAMETER Foreground
    Run the server in this window (Ctrl+C to stop) instead of in the background.

.PARAMETER Port
    TCP port to bind. Defaults to 8000.

.PARAMETER Reinstall
    Delete and rebuild .venv from scratch.

.EXAMPLE
    .\install_and_run.ps1
.EXAMPLE
    .\install_and_run.ps1 -Foreground -Port 8080
#>
[CmdletBinding()]
param(
    [switch]$Foreground,
    [int]$Port = 8000,
    [switch]$Reinstall
)

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

$venvPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$logFile    = Join-Path $PSScriptRoot 'logs\server.log'
$errFile    = Join-Path $PSScriptRoot 'logs\server.err.log'

# --- 1. Locate a usable Python interpreter -----------------------------------
function Get-BasePython {
    foreach ($candidate in @('python', 'py')) {
        $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($cmd) {
            $version = & $cmd.Source --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Using $($cmd.Source) ($version)" -ForegroundColor DarkGray
                return $cmd.Source
            }
        }
    }
    throw 'Python 3.10+ was not found on PATH. Install it from https://python.org and re-run.'
}

# --- 2. Build the virtual environment ----------------------------------------
if ($Reinstall -and (Test-Path '.venv')) {
    Write-Host 'Removing existing .venv...' -ForegroundColor Yellow
    Remove-Item '.venv' -Recurse -Force
}

if (-not (Test-Path $venvPython)) {
    $basePython = Get-BasePython
    Write-Host 'Creating virtual environment (.venv)...' -ForegroundColor Cyan
    & $basePython -m venv .venv
    if (-not (Test-Path $venvPython)) {
        throw "Failed to create .venv. Ensure the 'venv' module is available."
    }
}

# --- 3. Install pinned dependencies ------------------------------------------
Write-Host 'Installing dependencies...' -ForegroundColor Cyan
& $venvPython -m pip install --upgrade pip --quiet --disable-pip-version-check
& $venvPython -m pip install -r requirements.txt --quiet --disable-pip-version-check
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed. See the pip output above.' }

# --- 4. Bootstrap configuration ----------------------------------------------
if ((-not (Test-Path '.env')) -and (Test-Path '.env.example')) {
    Copy-Item '.env.example' '.env'
    Write-Host 'Created .env from .env.example — add your API keys before going public.' -ForegroundColor Yellow
}

New-Item -ItemType Directory -Path 'logs' -Force | Out-Null
New-Item -ItemType Directory -Path 'data' -Force | Out-Null

# --- 5. Fail fast if the app cannot even import ------------------------------
$env:PYTHONPATH = $PSScriptRoot
Write-Host 'Verifying application imports...' -ForegroundColor Cyan
& $venvPython -c 'import app.main'
if ($LASTEXITCODE -ne 0) { throw 'app/main.py failed to import. Fix the error above before starting the server.' }

# --- 6. Refuse to double-bind the port ---------------------------------------
$inUse = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($inUse) {
    throw "Port $Port is already in use (PID $($inUse[0].OwningProcess)). Stop it or pass -Port <other>."
}

# --- 7. Serve -----------------------------------------------------------------
$uvicornArgs = @('-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', "$Port")

if ($Foreground) {
    Write-Host "Serving on http://localhost:$Port (Ctrl+C to stop)" -ForegroundColor Green
    & $venvPython @uvicornArgs
    return
}

Write-Host 'Starting server in the background...' -ForegroundColor Cyan
$proc = Start-Process -FilePath $venvPython `
                      -ArgumentList $uvicornArgs `
                      -WorkingDirectory $PSScriptRoot `
                      -RedirectStandardOutput $logFile `
                      -RedirectStandardError $errFile `
                      -WindowStyle Hidden `
                      -PassThru

# --- 8. Wait for the health endpoint to actually answer ----------------------
# Probe 127.0.0.1, not "localhost": on Windows "localhost" resolves to ::1 first,
# but uvicorn bound to 0.0.0.0 listens on IPv4 only, so the IPv6 attempt refuses.
$healthUrl = "http://127.0.0.1:$Port/health"
$ready = $false
foreach ($attempt in 1..40) {
    if ($proc.HasExited) { break }
    try {
        $response = Invoke-RestMethod -Uri $healthUrl -TimeoutSec 3 -ErrorAction Stop
        if ($response.status -eq 'ok') { $ready = $true; break }
    } catch {
        # Not up yet (connection refused) — keep waiting.
    }
    Start-Sleep -Milliseconds 500
}

if (-not $ready) {
    Write-Host 'Server did not become healthy. Recent errors:' -ForegroundColor Red
    if (Test-Path $errFile) { Get-Content $errFile -Tail 30 }
    if (-not $proc.HasExited) { Stop-Process -Id $proc.Id -Force -Confirm:$false }
    throw "Startup failed. Full log: $errFile"
}

Write-Host ''
Write-Host 'EYRIC RYTHOS AI is running.' -ForegroundColor Green
Write-Host "  Dashboard : http://127.0.0.1:$Port/" -ForegroundColor Green
Write-Host "  Health    : $healthUrl" -ForegroundColor Green
Write-Host "  API docs  : http://127.0.0.1:$Port/docs" -ForegroundColor Green
Write-Host "  PID       : $($proc.Id)   (stop with: Stop-Process -Id $($proc.Id))" -ForegroundColor DarkGray
Write-Host "  Logs      : $logFile" -ForegroundColor DarkGray
