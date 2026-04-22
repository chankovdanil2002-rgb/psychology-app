$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendPath = Join-Path $projectRoot "backend"
$pythonPath = Join-Path $projectRoot ".venv\Scripts\python.exe"
$pgCtlPath = "C:\Program Files\PostgreSQL\18\bin\pg_ctl.exe"
$pgDataPath = Join-Path $projectRoot "local_pgdata"
$pgLogPath = Join-Path $projectRoot "local_pg.log"

if (-not (Test-Path $pythonPath)) {
    throw "Python virtual environment was not found: $pythonPath"
}

if ((Test-Path $pgCtlPath) -and (Test-Path $pgDataPath)) {
    & $pgCtlPath -D $pgDataPath status *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Starting local PostgreSQL on port 5433..."
        & $pgCtlPath -D $pgDataPath -l $pgLogPath -o "-p 5433" start | Out-Host
    }
}

Write-Host "Applying migrations..."
& $pythonPath (Join-Path $backendPath "manage.py") migrate

Write-Host "Seeding demo data..."
& $pythonPath (Join-Path $backendPath "seed_demo.py")

Write-Host "Starting Django server on http://127.0.0.1:8000"
& $pythonPath (Join-Path $backendPath "manage.py") runserver 127.0.0.1:8000
