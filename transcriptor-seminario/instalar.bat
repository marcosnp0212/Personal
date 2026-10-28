@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Instalando Python 3.12...
  winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
  echo.
  echo Python instalado. CIERRA esta ventana y vuelve a abrir instalar.bat
  pause
  exit /b
)
py -3.12 -m venv venv 2>nul || py -m venv venv
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\python -m pip install faster-whisper fastapi uvicorn python-multipart nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*"
echo.
echo Instalacion terminada. Ahora abre arrancar.bat
pause
