@echo off
chcp 65001 >nul
echo ========================================
echo    心理Z导航 - 公众号发布系统
echo ========================================
echo.
echo 正在启动系统...
echo.
cd /d "%~dp0"
python test_wechat_config.py
if errorlevel 1 (
    echo.
    echo 配置测试失败，请检查配置
    pause
    exit /b 1
)
echo.
echo 按任意键启动公众号发布系统...
pause >nul
python wechat_main.py
