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
    Write-Host '== JavaScript page logic (js-tests/page-logic.js) =='
    & $node --test-reporter=spec (Join-Path $app 'js-tests\page-logic.js')
    if ($LASTEXITCODE) { $failed = $true }
    Write-Host '== JavaScript rack BOM (js-tests/rack-bom.js) =='
    & $node --test-reporter=spec (Join-Path $app 'js-tests\rack-bom.js')
    if ($LASTEXITCODE) { $failed = $true }
    Write-Host '== JavaScript equipment rebuild (js-tests/equipment-rebuild.js) =='
    & $node --test-reporter=spec (Join-Path $app 'js-tests\equipment-rebuild.js')
    if ($LASTEXITCODE) { $failed = $true }
    Write-Host '== JavaScript equipment wizard steps (js-tests/equipment-wizard-steps.js) =='
    & $node --test-reporter=spec (Join-Path $app 'js-tests\equipment-wizard-steps.js')
    if ($LASTEXITCODE) { $failed = $true }
    Write-Host '== JavaScript Place on tray window (js-tests/tray-placement.js) =='
    & $node --test-reporter=spec (Join-Path $app 'js-tests\tray-placement.js')
    if ($LASTEXITCODE) { $failed = $true }
    Write-Host '== JavaScript cable routes (js-tests/cable-routes.js) =='
    & $node --test-reporter=spec (Join-Path $app 'js-tests\cable-routes.js')
    if ($LASTEXITCODE) { $failed = $true }
    Write-Host '== JavaScript cable suggestions (js-tests/cable-suggest.js) =='
    & $node --test-reporter=spec (Join-Path $app 'js-tests\cable-suggest.js')
    if ($LASTEXITCODE) { $failed = $true }
    Write-Host '== JavaScript cable sheet (js-tests/cable-sheet.js) =='
    & $node --test-reporter=spec (Join-Path $app 'js-tests\cable-sheet.js')
    if ($LASTEXITCODE) { $failed = $true }
    Write-Host '== JavaScript wiring sheet drawing (js-tests/cable-sheet-view.js) =='
    & $node --test-reporter=spec (Join-Path $app 'js-tests\cable-sheet-view.js')
    if ($LASTEXITCODE) { $failed = $true }
} else {
    Write-Host 'Node.js not found; JavaScript checks SKIPPED.'
    $failed = $true
}
if ($failed) { Write-Host 'RESULT: FAILED or incomplete'; exit 1 } else { Write-Host 'RESULT: all checks passed' }
