@echo off
title Practica Cifrado - Redes y Seguridad
echo ==============================================================================
echo    PRACTICA DE REDES Y SEGURIDAD - SISTEMA DE CIFRADO (WAN)
echo    Cesar, Vigenere y Vernam (One-Time Pad)
echo ==============================================================================
echo.
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo [*] Creando entorno virtual e instalando dependencias...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
)

echo.
echo [*] Iniciando aplicacion web en el puerto 5000...
echo.
echo   - Panel Principal / Topologia : http://localhost:5000/
echo   - PC 1 (Emisor - Laptop 1)    : http://localhost:5000/sender
echo   - PC 2 (Receptor - Laptop 2)  : http://localhost:5000/receiver
echo.
python app.py
pause
