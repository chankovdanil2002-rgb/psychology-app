$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendPath = Join-Path $projectRoot "frontend"
$nodePath = "C:\Program Files\nodejs\node.exe"
$npmCliPath = "C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js"
$nodeDir = Split-Path -Parent $nodePath

if (-not (Test-Path $nodePath)) {
    throw "Node.js was not found: $nodePath"
}

if (-not (Test-Path $npmCliPath)) {
    throw "npm CLI was not found: $npmCliPath"
}

Write-Host "Starting Vite dev server on http://127.0.0.1:3000"
Push-Location $frontendPath
try {
    $env:PATH = "$nodeDir;$env:PATH"
    & $nodePath $npmCliPath run dev -- --host 127.0.0.1 --port 3000
} finally {
    Pop-Location
}
