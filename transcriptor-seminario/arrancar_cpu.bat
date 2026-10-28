@echo off
chcp 65001 >nul
cd /d "%~dp0"
set WHISPER_DEVICE=cpu
venv\Scripts\python servidor_whisper.py
pause
