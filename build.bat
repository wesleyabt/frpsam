@echo off
chcp 65001 > nul
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║       Samsung ADB Master v2.0 - Build Script                  ║
echo ║       Windows 10/11 Executable Compiler                       ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ ERRO: Python não encontrado!
    echo   Instale Python 3.10+ em: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✓ Python detectado

echo.
echo [2/4] Instalando dependências...
pip install -q customtkinter pyserial pyinstaller qrcode pillow darkdetect
if errorlevel 1 (
    echo ✗ ERRO: Falha ao instalar dependências
    pause
    exit /b 1
)
echo ✓ Dependências instaladas

echo.
echo [3/4] Compilando executável...
echo   Nome: SamsungADBMaster.exe
echo   Tipo: Aplicação Windows (sem console)
echo   Modo: One-file (tudo em um arquivo)
echo.

pyinstaller --noconfirm --onefile --windowed ^
    --name "SamsungADBMaster" ^
    --add-data "samsung_helper.ps1;." ^
    --icon=NONE ^
    --distpath "dist" ^
    --buildpath "build" ^
    --specpath "." ^
    main.py

if errorlevel 1 (
    echo ✗ ERRO: Falha ao compilar com PyInstaller
    echo   Verifique se main.py e samsung_logic.py estão presentes
    pause
    exit /b 1
)

echo.
echo [4/4] Verificando arquivo gerado...
if exist "dist\SamsungADBMaster.exe" (
    echo.
    echo ╔═══════════════════════════════════════════════════════════════╗
    echo ║                  ✓ BUILD CONCLUÍDO COM SUCESSO!               ║
    echo ╠═══════════════════════════════════════════════════════════════╣
    echo ║                                                               ║
    echo ║  Executável gerado:  dist\SamsungADBMaster.exe                ║
    echo ║  Tamanho aproximado: 80-100 MB                               ║
    echo ║                                                               ║
    echo ║  PRÓXIMAS ETAPAS:                                            ║
    echo ║  1. Procure "dist\SamsungADBMaster.exe"                      ║
    echo ║  2. Execute o arquivo                                        ║
    echo ║  3. Conecte seu Samsung e ative o modo de teste (*#0*#)     ║
    echo ║  4. Clique em "EXECUTAR FLUXO COMPLETO"                     ║
    echo ║                                                               ║
    echo ║  DISTRIBUIR:                                                 ║
    echo ║  - Você pode compartilhar SamsungADBMaster.exe              ║
    echo ║  - Não é necessário Python instalado para usar               ║
    echo ║  - Requer: Windows 10/11, Drivers Samsung USB                ║
    echo ║                                                               ║
    echo ╚═══════════════════════════════════════════════════════════════╝
    echo.
) else (
    echo ✗ ERRO: Executável não foi gerado!
    echo   Verifique os logs acima para mais detalhes
    pause
    exit /b 1
)

echo Pressione qualquer tecla para fechar...
pause >nul
