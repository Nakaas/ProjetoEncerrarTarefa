@echo off
chcp 65001 >nul

echo Verificando instalação do Python. Aguarde...

python --version >nul 2>nul
if %ERRORLEVEL% == 0 (
    goto verificar_bibliotecas
) else (
    echo Python não encontrado. Instalando...
    mshta "javascript:alert('Python não encontrado. Iniciando a instalação...');close();"
    
    curl -o python-installer.exe https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe
    if not exist python-installer.exe (
        echo Falha ao baixar o instalador. Verifique sua conexão.
        exit /b
    )
    
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    
    echo Verificando instalação do Python. Aguarde...
    timeout /t 5 >nul
    
    python --version >nul 2>nul
    if %ERRORLEVEL% == 0 (
        echo Python instalado com sucesso.
        goto verificar_bibliotecas
    ) else (
        mshta "javascript:alert('Tente executar novamente o App, caso não funcione verifique as permissões ou instale manualmente!');close();"
        exit /b
    )
)

:verificar_bibliotecas
echo Verificando bibliotecas necessárias...
python -c "import psutil, tkinter, collections, subprocess" >nul 2>nul
if %ERRORLEVEL% == 0 (
    goto rodar_programa
) else (
    echo Instalando bibliotecas necessárias...
    pip install psutil >nul
)

:rodar_programa
echo Iniciando o programa...
start pythonw NK.pyw
exit /b
