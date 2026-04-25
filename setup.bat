@echo off
:: K10 Chat — Configuração Automática (Windows)
:: Uso: setup.bat <URL_DO_RENDER>
:: Ex:  setup.bat k10-signaling.onrender.com

if "%~1"=="" (
    echo.
    echo ============================================================
    echo   K10 Chat — Configuracao Automatica
    echo ============================================================
    echo.
    echo   Arraste e solte este arquivo no Prompt de Comando e
    echo   adicione a URL do seu servidor Render no final.
    echo.
    echo   Exemplo:
    echo   setup.bat k10-signaling.onrender.com
    echo.
    echo   Ou edite este arquivo e coloque sua URL abaixo:
    echo   set SIGNAL_URL=SUA_URL_AQUI
    echo.
    pause
    exit /b 1
)

python3 setup.py %1
if errorlevel 1 (
    python setup.py %1
)
pause
