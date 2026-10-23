# Builds a personal portable zip of the Assembly Workshop app (Brian, 2026-10-22).
# Personal use only: contains licensed third-party parts (see THIRD_PARTY_LOCAL_ONLY.md); do not redistribute.
# Excludes all user data; the zip starts with a fresh library in its own user-data folder.
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
$app = Join-Path $repo 'outputs\Mechanical_Design_App'
$stamp = Get-Date -Format 'yyyy-MM-dd_HHmm'
$outDir = Join-Path $repo 'outputs\Portable_Packages'
$stage = Join-Path $env:TEMP "aw-package-$stamp\AssemblyWorkshop"
New-Item -ItemType Directory -Force $stage, $outDir | Out-Null

robocopy $app "$stage\app" /E /XD data __pycache__ js-tests /XF *.pyc start.bat /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy failed ($LASTEXITCODE)" }

@'
@echo off
cd /d "%~dp0app"
set PY=
where python >nul 2>nul && set PY=python
if exist "C:\Program Files\Python310\python.exe" set PY="C:\Program Files\Python310\python.exe"
if not defined PY (echo Python 3.10+ not found. Install it from python.org. & pause & exit /b 1)
start "" http://127.0.0.1:8765
%PY% app.py --data "%~dp0user-data"
pause
'@ | Set-Content -Encoding ascii "$stage\Start Assembly Workshop.bat"

@"
Assembly Workshop - portable copy (built $stamp from commit $(git -C $repo rev-parse --short HEAD))
PERSONAL USE ONLY. Contains licensed third-party parts; do not share.

1. Unzip anywhere.
2. Needs Python 3.10+ (python.org) and OpenSCAD (for STL builds). FreeCAD only for STEP import.
3. Double-click "Start Assembly Workshop.bat". The browser opens http://127.0.0.1:8765
   (refresh once if it opened before the app was ready).
4. Your designs are saved in the user-data folder next to this file. Back it up to keep them.
   To use your main library instead, copy data\normal-use from the repo into user-data.
"@ | Set-Content -Encoding utf8 "$stage\README.txt"

$zip = Join-Path $outDir "AssemblyWorkshop_Portable_$stamp.zip"
Compress-Archive -Path $stage -DestinationPath $zip
Remove-Item -Recurse -Force (Split-Path $stage -Parent)
Get-Item $zip | Select-Object FullName, @{n='MB';e={[math]::Round($_.Length/1MB,1)}}
