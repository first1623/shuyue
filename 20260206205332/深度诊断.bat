@echo off
chcp 65001 > nul
cls
echo ========================================
echo Python 深度诊断工具
echo ========================================
echo.

echo [1/6] 检查python命令...
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ 找到python命令
    for /f "tokens=*" %%i in ('where python') do (
        echo   路径: %%i
        "%%i" --version 2>nul
    )
) else (
    echo ✗ 未找到python命令
)

echo.
echo [2/6] 检查python3命令...
where python3 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ 找到python3命令
    for /f "tokens=*" %%i in ('where python3') do (
        echo   路径: %%i
        "%%i" --version 2>nul
    )
) else (
    echo ✗ 未找到python3命令
)

echo.
echo [3/6] 检查py命令...
where py >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ 找到py命令
    for /f "tokens=*" %%i in ('where py') do (
        echo   路径: %%i
        "%%i" --version 2>nul
    )
) else (
    echo ✗ 未找到py命令
)

echo.
echo [4/6] 搜索常见Python安装位置...

if exist "C:\Python39\python.exe" (
    echo ✓ 找到: C:\Python39\python.exe
    C:\Python39\python.exe --version
)

if exist "C:\Python310\python.exe" (
    echo ✓ 找到: C:\Python310\python.exe
    C:\Python310\python.exe --version
)

if exist "C:\Python311\python.exe" (
    echo ✓ 找到: C:\Python311\python.exe
    C:\Python311\python.exe --version
)

if exist "C:\Python312\python.exe" (
    echo ✓ 找到: C:\Python312\python.exe
    C:\Python312\python.exe --version
)

if exist "C:\Program Files\Python39\python.exe" (
    echo ✓ 找到: C:\Program Files\Python39\python.exe
    "C:\Program Files\Python39\python.exe" --version
)

if exist "C:\Program Files\Python310\python.exe" (
    echo ✓ 找到: C:\Program Files\Python310\python.exe
    "C:\Program Files\Python310\python.exe" --version
)

if exist "C:\Program Files\Python311\python.exe" (
    echo ✓ 找到: C:\Program Files\Python311\python.exe
    "C:\Program Files\Python311\python.exe" --version
)

if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe" (
    echo ✓ 找到: %USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe
    "%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe" --version
)

if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python310\python.exe" (
    echo ✓ 找到: %USERPROFILE%\AppData\Local\Programs\Python\Python310\python.exe
    "%USERPROFILE%\AppData\Local\Programs\Python\Python310\python.exe" --version
)

if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe" (
    echo ✓ 找到: %USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe
    "%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe" --version
)

if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe" (
    echo ✓ 找到: %USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe
    "%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe" --version
)

echo.
echo [5/6] 检查Anaconda/Miniconda...
if exist "%USERPROFILE%\anaconda3\python.exe" (
    echo ✓ 找到Anaconda: %USERPROFILE%\anaconda3\python.exe
    "%USERPROFILE%\anaconda3\python.exe" --version
)

if exist "%USERPROFILE%\miniconda3\python.exe" (
    echo ✓ 找到Miniconda: %USERPROFILE%\miniconda3\python.exe
    "%USERPROFILE%\miniconda3\python.exe" --version
)

echo.
echo [6/6] 检查WindowsApps中的Python...
dir "%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\python*.exe" /b 2>nul
if %errorlevel% equ 0 (
    echo 找到WindowsApps中的Python文件
    echo 注意：这些可能是应用商店的占位符，不是完整安装
)

echo.
echo ========================================
echo PATH环境变量检查
echo ========================================
echo %PATH%

echo.
echo ========================================
echo 诊断完成
echo ========================================
echo.

echo 解决方案：
echo.

REM 检查是否找到了Python
set PYTHON_FOUND=0

if exist "C:\Python39\python.exe" (
    set PYTHON_FOUND=1
    echo 方案1: 使用完整路径
    echo   C:\Python39\python.exe launcher.py
    echo.
)

if exist "C:\Python310\python.exe" (
    set PYTHON_FOUND=1
    echo 方案2: 使用完整路径
    echo   C:\Python310\python.exe launcher.py
    echo.
)

if exist "C:\Python311\python.exe" (
    set PYTHON_FOUND=1
    echo 方案3: 使用完整路径
    echo   C:\Python311\python.exe launcher.py
    echo.
)

if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe" (
    set PYTHON_FOUND=1
    echo 方案4: 使用完整路径
    echo   %USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe launcher.py
    echo.
)

if "%PYTHON_FOUND%"=="0" (
    echo 未找到Python安装！
    echo 请按照 "Python安装指南.md" 安装Python
    echo.
    echo 或访问: https://www.python.org/downloads/
)

echo ========================================
pause
