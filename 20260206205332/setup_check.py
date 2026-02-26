#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""项目完整性检查"""

import os
import sys

def check_file(path, description):
    """检查文件是否存在"""
    if os.path.exists(path):
        print(f"  ✓ {description}: {path}")
        return True
    else:
        print(f"  ✗ {description}: {path} (缺失)")
        return False

def main():
    print("=" * 70)
    print("项目完整性检查".center(70))
    print("=" * 70)
    print()

    # 检查文件
    print("[1/4] 检查核心文件:")
    files = [
        ("config.py", "配置文件"),
        ("logger.py", "日志模块"),
        ("ai_client.py", "AI客户端"),
        ("xiaohongshu_publisher.py", "主系统"),
        ("main.py", "主程序入口"),
        (".env", "环境配置"),
        ("requirements.txt", "依赖列表"),
    ]

    for filename, desc in files:
        check_file(filename, desc)

    print()

    # 检查智能体模块
    print("[2/4] 检查智能体模块:")
    agents = [
        ("agents/__init__.py", "智能体初始化"),
        ("agents/planner.py", "策划智能体"),
        ("agents/writer.py", "文案智能体"),
        ("agents/designer.py", "图片智能体"),
        ("agents/reviewer.py", "审核智能体"),
        ("agents/publisher.py", "发布智能体"),
    ]

    for filename, desc in agents:
        check_file(filename, desc)

    print()

    # 检查目录
    print("[3/4] 检查目录:")
    dirs = [
        ("logs", "日志目录"),
        ("generated_images", "图片生成目录"),
        ("publish_records", "发布记录目录"),
        ("agents", "智能体模块目录"),
    ]

    for dirname, desc in dirs:
        if os.path.isdir(dirname):
            print(f"  ✓ {desc}: {dirname}/")
        else:
            print(f"  ✗ {desc}: {dirname}/ (缺失)")

    print()

    # 检查Python版本
    print("[4/4] 检查Python环境:")
    print(f"  Python版本: {sys.version}")
    print(f"  Python路径: {sys.executable}")
    print()

    # 检查依赖
    print("检查依赖包:")
    try:
        import openai
        print(f"  ✓ openai: {openai.__version__}")
    except ImportError:
        print(f"  ✗ openai: 未安装")

    try:
        from dotenv import load_dotenv
        print(f"  ✓ python-dotenv: 已安装")
    except ImportError:
        print(f"  ✗ python-dotenv: 未安装")

    try:
        import requests
        print(f"  ✓ requests: {requests.__version__}")
    except ImportError:
        print(f"  ✗ requests: 未安装")

    try:
        from PIL import Image
        print(f"  ✓ Pillow: {Image.__version__}")
    except ImportError:
        print(f"  ✗ Pillow: 未安装")

    print()
    print("=" * 70)
    print("检查完成！".center(70))
    print("=" * 70)
    print()

    # 检查配置
    print("配置检查:")
    try:
        from config import Config
        print(f"  ✓ 配置加载成功")
        print(f"  AI提供商: {Config.AI_PROVIDER}")

        if Config.AI_PROVIDER == 'deepseek':
            key = Config.DEEPSEEK_API_KEY
            if key:
                masked = key[:10] + "*" * (len(key) - 10)
                print(f"  DeepSeek API Key: {masked}")
            else:
                print(f"  ✗ DeepSeek API Key: 未配置")

    except Exception as e:
        print(f"  ✗ 配置错误: {str(e)}")

    print()
    print("=" * 70)
    print()

    # 建议
    missing_deps = False
    try:
        import openai
        from dotenv import load_dotenv
        import requests
        from PIL import Image
    except ImportError:
        missing_deps = True

    if missing_deps:
        print("建议操作:")
        print("  1. 安装依赖: pip install -r requirements.txt")
        print("     或运行: python check_and_install.py")
        print()

    print("下一步操作:")
    print("  1. 测试API连接: python test_connection.py")
    print("  2. 启动系统: python main.py")
    print("  3. 或使用启动脚本: start.bat (Windows)")
    print()

if __name__ == '__main__':
    main()
