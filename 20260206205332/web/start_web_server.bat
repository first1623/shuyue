@echo off
chcp 65001 >nul
title 心理Z导航 - Web服务器
cd /d "%~dp0"

echo ========================================
echo    启动Web服务器
echo ========================================
echo.
echo 正在检查依赖...

py -c "import flask" 2>nul
if errorlevel 1 (
    echo.
    echo Flask未安装，正在安装...
    pip install flask flask-cors
    echo.
)

py -c "import openai" 2>nul
if errorlevel 1 (
    echo.
    echo OpenAI未安装，正在安装...
    pip install openai
    echo.
)

echo 正在启动服务器...
echo.
echo ========================================
echo   访问地址: http://localhost:5000
echo ========================================
echo.
echo 提示：启动后会自动打开浏览器
echo.

py api_server.py

pause
