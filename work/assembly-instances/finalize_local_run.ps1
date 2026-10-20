$ErrorActionPreference = 'Stop'
foreach ($testTarget in @(@{Id=13288; Pattern='*preview_server.py*'},@{Id=31148; Pattern='*visualize*render.py*rack-studio-options.html*8768*'})) {
    $testOwner = Get-CimInstance Win32_Process -Filter ("ProcessId = " + $testTarget.Id)
    if ($testOwner) {
        if ($testOwner.CommandLine -notlike $testTarget.Pattern) { throw 'A disposable server process changed identity; it was not stopped.' }
        Stop-Process -Id $testTarget.Id
    }
}
$normalStatus = Invoke-RestMethod -Uri 'http://127.0.0.1:8765/api/workspace-capabilities' -TimeoutSec 5
if ($normalStatus.version -ne 2 -or !$normalStatus.independent_assemblies) { throw 'Normal-use capability check failed.' }
Add-Content -LiteralPath 'C:\Users\brian\.codex\automations\recover-lab-rax-rack-builder-geometry\memory.md' -Value (Get-Content -LiteralPath 'work\assembly-instances\Memory_Append.md' -Raw -Encoding utf8) -Encoding utf8
Write-Output 'Stopped only the two verified temporary servers. Normal app v2 remains running. Appended automation memory.'
