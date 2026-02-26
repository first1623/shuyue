#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查并安装依赖"""

import subprocess
import sys

def check_package(package_name):
    """检查包是否已安装"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """安装包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("=" * 60)
    print("检查并安装依赖包")
    print("=" * 60)
    print()

    # 需要的包
    packages = [
        ("openai", "openai>=1.0.0"),
        ("dotenv", "python-dotenv>=1.0.0"),
        ("requests", "requests>=2.31.0"),
        ("PIL", "Pillow>=10.0.0"),
    ]

    installed = []
    missing = []

    for import_name, package_name in packages:
        if check_package(import_name):
            print(f"✓ {package_name} 已安装")
            installed.append(package_name)
        else:
            print(f"✗ {package_name} 未安装")
            missing.append(package_name)

    print()
    print("=" * 60)
    print(f"已安装: {len(installed)} 个")
    print(f"缺少: {len(missing)} 个")
    print("=" * 60)
    print()

    if missing:
        print("正在安装缺失的包...")
        print()

        for package in missing:
            print(f"安装 {package}...")
            if install_package(package):
                print(f"✓ {package} 安装成功")
            else:
                print(f"✗ {package} 安装失败")

        print()
        print("=" * 60)
        print("依赖安装完成！")
        print("=" * 60)
        print()
        print("现在可以运行:")
        print("  python test_connection.py  # 测试API连接")
        print("  python main.py            # 运行主程序")
    else:
        print("所有依赖已安装！")
        print()
        print("现在可以运行:")
        print("  python test_connection.py  # 测试API连接")
        print("  python main.py            # 运行主程序")

if __name__ == '__main__':
    main()
