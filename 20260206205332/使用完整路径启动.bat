@echo off
chcp 65001 > nul
echo ========================================
echo 小红书发布系统 - 使用完整路径启动
echo ========================================
echo.

REM 尝试查找Python

if exist "C:\Python39\python.exe" (
    echo 使用Python: C:\Python39\python.exe
    echo.
    cd /d "%~dp0"
    C:\Python39\python.exe launcher.py
    goto end
)

if exist "C:\Python310\python.exe" (
    echo 使用Python: C:\Python310\python.exe
    echo.
    cd /d "%~dp0"
    C:\Python310\python.exe launcher.py
    goto end
)

if exist "C:\Python311\python.exe" (
    echo 使用Python: C:\Python311\python.exe
    echo.
    cd /d "%~dp0"
    C:\Python311\python.exe launcher.py
    goto end
)

if exist "C:\Python312\python.exe" (
    echo 使用Python: C:\Python312\python.exe
    echo.
    cd /d "%~dp0"
    C:\Python312\python.exe launcher.py
    goto end
)

if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe" (
    echo 使用Python: %USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe
    echo.
    cd /d "%~dp0"
    "%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe" launcher.py
    goto end
)

if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python310\python.exe" (
    echo 使用Python: %USERPROFILE%\AppData\Local\Programs\Python\Python310\python.exe
    echo.
    cd /d "%~dp0"
    "%USERPROFILE%\AppData\Local\Programs\Python\Python310\python.exe" launcher.py
    goto end
)

if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe" (
    echo 使用Python: %USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe
    echo.
    cd /d "%~dp0"
    "%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe" launcher.py
    goto end
)

if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe" (
    echo 使用Python: %USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe
    echo.
    cd /d "%~dp0"
    "%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe" launcher.py
    goto end
)

if exist "%USERPROFILE%\anaconda3\python.exe" (
    echo 使用Anaconda: %USERPROFILE%\anaconda3\python.exe
    echo.
    cd /d "%~dp0"
    "%USERPROFILE%\anaconda3\python.exe" launcher.py
    goto end
)

if exist "%USERPROFILE%\miniconda3\python.exe" (
    echo 使用Miniconda: %USERPROFILE%\miniconda3\python.exe
    echo.
    cd /d "%~dp0"
    "%USERPROFILE%\miniconda3\python.exe" launcher.py
    goto end
)

echo ========================================
echo 错误：未找到Python安装！
echo ========================================
echo.
echo 请先安装Python：
echo 1. 访问 https://www.python.org/downloads/
echo 2. 下载Windows安装程序
echo 3. 安装时务必勾选 "Add Python to PATH"
echo.

:end
pause
