@echo off
cd /d "%~dp0"
"C:\Program Files\Python310\python.exe" app.py --existing-library --data "%~dp0..\..\data\normal-use"
pause
