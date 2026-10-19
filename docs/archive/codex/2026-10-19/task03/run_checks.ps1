# Rerunnable checks: targeted Python tests incl. faceplate color (temporary data only) + JavaScript module tests.
# Starts no server, touches no user data, runs no OpenSCAD build. Usage: powershell -File run_checks.ps1
$ErrorActionPreference = 'Stop'
$app = $PSScriptRoot
$project = (Resolve-Path (Join-Path $app '..\..')).Path
$python = 'C:\Program Files\Python310\python.exe'
$node = (Get-Command node -ErrorAction SilentlyContinue).Source
if (-not $node) {
    $fallback = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
    if (Test-Path $fallback) { $node = $fallback }
}
$failed = $false
Write-Host '== Python (work/gui-refinement/check_python.py) =='
& $python -B (Join-Path $project 'work\gui-refinement\check_python.py')
if ($LASTEXITCODE) { $failed = $true }
Write-Host '== JavaScript (js-tests/run.js) =='
if ($node) {
    & $node --test-reporter=spec (Join-Path $app 'js-tests\run.js')
    if ($LASTEXITCODE) { $failed = $true }
} else {
    Write-Host 'Node.js not found; JavaScript checks SKIPPED.'
    $failed = $true
}
if ($failed) { Write-Host 'RESULT: FAILED or incomplete'; exit 1 } else { Write-Host 'RESULT: all checks passed' }
