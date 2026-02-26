@echo off
chcp 65001 > nul
echo ========================================
echo 小红书多智能体内容生成系统 - 启动脚本
echo ========================================
echo.

echo [1/3] 检查依赖...
python check_and_install.py
if %errorlevel% neq 0 (
    echo.
    echo 依赖检查失败，请手动运行: python check_and_install.py
    pause
    exit /b 1
)

echo.
echo [2/3] 测试API连接...
python test_connection.py
if %errorlevel% neq 0 (
    echo.
    echo API连接测试失败，请检查.env配置
    pause
    exit /b 1
)

echo.
echo [3/3] 启动主程序...
python main.py

pause
