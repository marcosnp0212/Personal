@echo off
chcp 65001 >nul
cd /d "%~dp0"
venv\Scripts\python servidor_whisper.py
echo.
echo Si ha salido un error de NVIDIA/cuda/cudnn, usa arrancar_cpu.bat
pause
