# Sets up a Windows machine with the same 3D part tools as the main PC.
# Run from the repo root in PowerShell:
#   powershell -NoProfile -ExecutionPolicy Bypass -File tools\setup_3d_tools.ps1 -CheckOnly   (report only)
#   powershell -NoProfile -ExecutionPolicy Bypass -File tools\setup_3d_tools.ps1              (install what's missing)
# Installs only what's missing: Git, Python 3.10, OpenSCAD 2021.01, FreeCAD (STEP import), the pinned OpenSCAD
# snapshot and the pinned Python packages. Never removes or overwrites anything that is already there.
param(
    [string]$ToolsRoot = $(if (Test-Path 'D:\') { 'D:\Tools' } else { 'C:\Tools' }),
    [switch]$CheckOnly,
    [switch]$SkipFreeCAD
)
$ErrorActionPreference = 'Continue'  # PowerShell 5.1 turns harmless stderr from pip or winget into errors; real failures throw below
$Repo = Split-Path -Parent $PSScriptRoot
$SnapName = 'OpenSCAD-2026.11.01-x86-64'
$SnapUrl = "https://files.openscad.org/snapshots/$SnapName.zip"
$SnapSha = 'ffa470450ba95e33ff68f9d0d4f29ca6c3e0df46a269fb670f12c0a19c442c13'  # openscad.exe on the main PC
$SnapExe = Join-Path $ToolsRoot "OpenSCAD-snapshot\$SnapName\openscad.exe"
$DefaultSnapExe = "D:\Tools\OpenSCAD-snapshot\$SnapName\openscad.exe"
$Packages = @('manifold3d==3.5.4', 'trimesh==5.1.1', 'numpy==2.2.6', 'shapely==2.1.2', 'pillow==12.3.0', 'matplotlib==3.10.9')
$script:Missing = 0

function Report($ok, $what, $detail) {
    if ($ok) { Write-Host "  OK       $what $detail" -ForegroundColor Green }
    else { Write-Host "  MISSING  $what $detail" -ForegroundColor Yellow; $script:Missing++ }
}

function Install-Winget($id, $version) {
    if ($CheckOnly) { return }
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw "winget not found: install App Installer from the Microsoft Store, then rerun." }
    $wingetArgs = @('install', '--id', $id, '-e', '--accept-package-agreements', '--accept-source-agreements')
    if ($version) { $wingetArgs += @('--version', $version) }
    Write-Host "  Installing $id ..."
    & winget @wingetArgs
}

function Find-Python {
    try { $v = & py -3.10 -c "import sys;print(sys.version.split()[0])" 2>$null; if ($LASTEXITCODE -eq 0 -and $v) { return @('py', '-3.10') } } catch {}
    try { $v = & python -c "import sys;print('%d.%d' % sys.version_info[:2])" 2>$null; if ($v -eq '3.10') { return @('python') } } catch {}
    return $null
}

Write-Host "Repo: $Repo"
Write-Host "Tools folder: $ToolsRoot"

# Git
$git = [bool](Get-Command git -ErrorAction SilentlyContinue)
Report $git 'Git' ''
if (-not $git) { Install-Winget 'Git.Git' $null }

# Python 3.10 (the app and tools target 3.10)
$py = Find-Python
Report ([bool]$py) 'Python 3.10' ''
if (-not $py) {
    Install-Winget 'Python.Python.3.10' $null
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
    $py = Find-Python
}

# Python packages, pinned to the main PC's versions
if ($py) {
    $pyExe = $py[0]; $pyArgs = @($py | Select-Object -Skip 1)
    $have = (& $pyExe @pyArgs -m pip list --format=freeze 2>$null) -join "`n"
    $need = @($Packages | Where-Object { $have -notmatch ("(?im)^" + [regex]::Escape($_) + "$") })
    Report ($need.Count -eq 0) 'Python packages' ($(if ($need.Count) { 'need: ' + ($need -join ' ') } else { '' }))
    if ($need.Count -and -not $CheckOnly) { & $pyExe @pyArgs -m pip install --user @need }
} else {
    Report $false 'Python packages' '(needs Python 3.10 first)'
}

# OpenSCAD 2021.01: the app, existing scripts and reproducing old revisions
$old = 'C:\Program Files\OpenSCAD\openscad.exe'
Report (Test-Path $old) 'OpenSCAD 2021.01' $old
if (-not (Test-Path $old)) { Install-Winget 'OpenSCAD.OpenSCAD' '2021.01' }

# FreeCAD: STEP import in the equipment wizard
if (-not $SkipFreeCAD) {
    $fc = @(Get-ChildItem 'C:\Program Files' -Directory -Filter 'FreeCAD*' -ErrorAction SilentlyContinue).Count -gt 0
    Report $fc 'FreeCAD' '(STEP import only; skip with -SkipFreeCAD)'
    if (-not $fc) { Install-Winget 'FreeCAD.FreeCAD' $null }
}

# Pinned OpenSCAD snapshot with Manifold: new parts
$snapOk = (Test-Path $SnapExe) -and ((Get-FileHash $SnapExe -Algorithm SHA256).Hash -eq $SnapSha)
Report $snapOk 'OpenSCAD snapshot' $SnapExe
if ((Test-Path $SnapExe) -and -not $snapOk) { throw "$SnapExe exists but is not the pinned build. Left it untouched; check it by hand." }
if (-not $snapOk -and -not $CheckOnly) {
    $dir = Join-Path $ToolsRoot 'OpenSCAD-snapshot'
    New-Item -ItemType Directory -Force $dir | Out-Null
    $zip = Join-Path $dir "$SnapName.zip"
    Write-Host "  Downloading $SnapUrl ..."
    Invoke-WebRequest $SnapUrl -OutFile $zip -UseBasicParsing
    Expand-Archive $zip -DestinationPath $dir
    Remove-Item $zip
    if ((Get-FileHash $SnapExe -Algorithm SHA256).Hash -ne $SnapSha) { throw "Downloaded snapshot doesn't match the main PC's build. Don't use it; tell Claude." }
}
if ($SnapExe -ne $DefaultSnapExe) {
    $set = [Environment]::GetEnvironmentVariable('AW_OPENSCAD_SNAPSHOT', 'User') -eq $SnapExe
    Report $set 'AW_OPENSCAD_SNAPSHOT' "(points the tools at $SnapExe)"
    if (-not $set -and -not $CheckOnly) {
        [Environment]::SetEnvironmentVariable('AW_OPENSCAD_SNAPSHOT', $SnapExe, 'User')
        $env:AW_OPENSCAD_SNAPSHOT = $SnapExe
    }
}

# Shared library is in the repo
Report ((Test-Path (Join-Path $Repo 'lib\workshop.scad')) -and (Test-Path (Join-Path $Repo 'lib\BOSL2\std.scad'))) 'Shared library' '(lib\ in the repo; run git pull if missing)'

if ($CheckOnly) {
    Write-Host "`n$script:Missing item(s) missing. Rerun without -CheckOnly to install them."
    exit $(if ($script:Missing) { 1 } else { 0 })
}

# Prove it works: render, check and package disposable test parts with both test suites
Write-Host "`nRunning the 3D tool tests ..."
$py = Find-Python
if (-not $py) { throw "Python 3.10 still not found. Open a new PowerShell window and rerun." }
$pyExe = $py[0]; $pyArgs = @($py | Select-Object -Skip 1)
Push-Location $Repo
try { & $pyExe @pyArgs -B -m unittest tools/test_release_part.py tools/test_workshop_lib.py; $code = $LASTEXITCODE } finally { Pop-Location }
if ($code -ne 0) { throw "Tests failed; paste the output to Claude." }
Write-Host "`nAll set. New tools installed by winget may need a new PowerShell window." -ForegroundColor Green
