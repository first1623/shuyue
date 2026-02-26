@echo off
chcp 65001 > nul
echo ========================================
echo 项目完整性检查
echo ========================================
echo.

cd /d "%~dp0"

echo 正在检查项目...
python3 setup_check.py

if %errorlevel% neq 0 (
    echo.
    echo 检查失败，可能需要先安装Python
    pause
    exit /b 1
)

echo.
echo ========================================
echo 按任意键继续...
pause > nul
