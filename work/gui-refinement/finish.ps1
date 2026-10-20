$ErrorActionPreference='Stop'
$testOwner=Get-CimInstance Win32_Process -Filter 'ProcessId = 34368'
if ($testOwner) {
    if ($testOwner.CommandLine -notlike '*preview_server.py*') { throw 'Disposable process changed; it was not stopped.' }
    Stop-Process -Id 34368
}
$caps=Invoke-RestMethod -Uri 'http://127.0.0.1:8765/api/workspace-capabilities' -TimeoutSec 5
if ($caps.studio_save_version -ne 1) { throw 'Normal server is not running the combined Save handler.' }
Add-Content -LiteralPath 'C:\Users\brian\.codex\automations\recover-lab-rax-rack-builder-geometry\memory.md' -Value (Get-Content -LiteralPath 'work/gui-refinement/Memory_Append.md' -Raw -Encoding utf8) -Encoding utf8
Write-Output 'Disposable server stopped; normal hybrid studio remains running. Automation memory updated.'
