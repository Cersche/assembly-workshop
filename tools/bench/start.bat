@echo off
setlocal
cd /d "%~dp0\..\.."
start "Workshop Bench" /b python -B tools\bench\bench.py --port 8720
start "" http://127.0.0.1:8720/
endlocal
