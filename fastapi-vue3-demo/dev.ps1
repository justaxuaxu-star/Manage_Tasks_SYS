Set-Location $PSScriptRoot
& "$PSScriptRoot\venv\Scripts\python.exe" -m backend.uvicorn_cli @args
exit $LASTEXITCODE