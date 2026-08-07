$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
python -m pip install -r requirements.txt
Start-Job -ScriptBlock {
    Set-Location $using:PSScriptRoot
    $env:PYTHONPATH = '.'
    python service.py
} | Out-Null
Write-Host 'EYRIC RYTHOS AI service started in the background.'
Write-Host 'Use http://localhost:8000/health to check the API.'
