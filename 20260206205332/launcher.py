#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""系统启动器 - 自动检查并启动"""

import os
import sys
import subprocess

def run_command(cmd, description):
    """运行命令"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        print(result.stdout)
        if result.stderr and "error" not in result.stderr.lower():
            print(result.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("操作超时")
        return False
    except Exception as e:
        print(f"错误: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("小红书多智能体内容生成系统 - 启动器".center(70))
    print("=" * 70)

    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 第1步：检查依赖
    print("\n[步骤 1/3] 检查并安装依赖")
    if not run_command("python setup_check.py", "运行项目检查"):
        print("依赖检查失败")

    # 第2步：测试连接
    print("\n[步骤 2/3] 测试API连接")
    test_input = input("是否测试DeepSeek API连接？(y/n，默认y): ").strip()
    if test_input.lower() != 'n':
        if not run_command("python test_connection.py", "测试API连接"):
            print("API连接测试失败，请检查.env配置")
            input("\n按回车键退出...")
            return

    # 第3步：启动主程序
    print("\n[步骤 3/3] 启动主程序")
    input("按回车键启动主程序...")

    try:
        # 直接导入并运行main.py
        import main
        main.main()
    except KeyboardInterrupt:
        print("\n\n程序已中断")
    except Exception as e:
        print(f"\n\n启动失败: {str(e)}")
        input("\n按回车键退出...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已退出")
    except Exception as e:
        print(f"\n\n启动器错误: {str(e)}")
        input("\n按回车键退出...")
