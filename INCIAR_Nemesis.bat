@echo off
title PROTOCOLO NEMESIS - SERVIDOR LOCAL
color 0A

echo ==================================================
echo    INICIANDO PROTOCOLO NEMESIS IA
echo ==================================================
echo.
echo [1/3] Verificando integridade do sistema...
echo [2/3] Ativando Camada Neural (Venv)...

:: Caminho relativo para ativar o ambiente virtual
call .\venv\Scripts\activate

echo [3/3] Carregando Interface Visual...
echo.
echo --------------------------------------------------
echo    O NAVEGADOR ABRIRA EM INSTANTES.
echo    NAO FECHE ESTA JANELA PRETA ENQUANTO USAR.
echo --------------------------------------------------
echo.

:: Lança o Streamlit
streamlit run nemesis_app.py

pause