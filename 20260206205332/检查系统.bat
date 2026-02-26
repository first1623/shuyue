@echo off
chcp 65001 > nul
echo ========================================
echo 系统Python检查
echo ========================================
echo.

echo [1/5] 检查Python安装...
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ 找到python命令
    python --version
) else (
    echo ✗ 未找到python命令
)

echo.
where python3 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ 找到python3命令
    python3 --version
) else (
    echo ✗ 未找到python3命令
)

echo.
where py >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ 找到py命令
    py --version
) else (
    echo ✗ 未找到py命令
)

echo.
echo [2/5] 检查Python安装位置...
if exist "C:\Python39" (
    echo ✓ 找到 C:\Python39
)
if exist "C:\Python310" (
    echo ✓ 找到 C:\Python310
)
if exist "C:\Python311" (
    echo ✓ 找到 C:\Python311
)
if exist "C:\Program Files\Python39" (
    echo ✓ 找到 C:\Program Files\Python39
)
if exist "C:\Program Files\Python310" (
    echo ✓ 找到 C:\Program Files\Python310
)
if exist "C:\Program Files\Python311" (
    echo ✓ 找到 C:\Program Files\Python311
)
if exist "%USERPROFILE%\AppData\Local\Programs\Python" (
    echo ✓ 找到 %USERPROFILE%\AppData\Local\Programs\Python
    dir "%USERPROFILE%\AppData\Local\Programs\Python" /b /ad
)

echo.
echo [3/5] 检查pip...
where pip >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ 找到pip
    pip --version
) else (
    echo ✗ 未找到pip
)

echo.
echo [4/5] 检查Anaconda...
if exist "%USERPROFILE%\anaconda3" (
    echo ✓ 找到 Anaconda: %USERPROFILE%\anaconda3
)
if exist "%USERPROFILE%\miniconda3" (
    echo ✓ 找到 Miniconda: %USERPROFILE%\miniconda3
)

echo.
echo [5/5] 检查Python相关路径...
dir "%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\python*" /b 2>nul

echo.
echo ========================================
echo 检查完成！
echo ========================================
echo.

if exist "C:\Python39\python.exe" (
    echo 找到Python，可以使用以下命令启动：
    echo C:\Python39\python.exe launcher.py
    echo.
)
if exist "C:\Python310\python.exe" (
    echo 找到Python，可以使用以下命令启动：
    echo C:\Python310\python.exe launcher.py
    echo.
)
if exist "C:\Python311\python.exe" (
    echo 找到Python，可以使用以下命令启动：
    echo C:\Python311\python.exe launcher.py
    echo.
)

echo 如果未找到Python，请按照 "Python安装指南.md" 安装Python
echo.

pause
