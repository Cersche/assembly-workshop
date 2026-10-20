$ErrorActionPreference='Stop'
$oldNormal=Get-CimInstance Win32_Process -Filter 'ProcessId = 19424'
if (!$oldNormal -or $oldNormal.CommandLine -notlike '*app.py*--existing-library*data\normal-use*8765*') { throw 'Normal-use server identity changed; no restart performed.' }
$socket=Get-NetTCPConnection -LocalPort 8765 -State Listen
if ($socket.OwningProcess -ne 19424) { throw 'Port8765 changed owner; no restart performed.' }
Stop-Process -Id 19424
$newNormal=Start-Process -FilePath 'C:\Program Files\Python310\python.exe' -ArgumentList @('-B','app.py','--existing-library','--data','"C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\data\normal-use"','--port','8765') -WorkingDirectory 'C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\outputs\Mechanical_Design_App' -WindowStyle Hidden -RedirectStandardOutput 'C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\gui-refinement\normal.stdout.log' -RedirectStandardError 'C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\work\gui-refinement\normal.stderr.log' -PassThru
Set-Content -LiteralPath 'work/gui-refinement/normal.pid' -Value $newNormal.Id -Encoding utf8
Write-Output $newNormal.Id
