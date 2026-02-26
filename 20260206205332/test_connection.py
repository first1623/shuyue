#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试DeepSeek API连接"""

import sys
import io

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from ai_client import AIClient

def main():
    print("=" * 60)
    print("DeepSeek API 连接测试")
    print("=" * 60)
    print()

    try:
        print("正在创建DeepSeek客户端...")
        client = AIClient('deepseek')

        print(f"API提供商: {client.provider}")
        print(f"模型: {client.model}")
        print()

        print("正在测试连接...")
        result = client.test_connection()

        print()
        if result:
            print("✅ 连接成功！")
            print()
            print("配置正确，可以使用以下命令运行系统：")
            print("  python main.py")
        else:
            print("❌ 连接失败")
            print()
            print("请检查：")
            print("1. API Key是否正确")
            print("2. 网络连接是否正常")
            print("3. 账户是否有余额")

    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        print()
        print("请检查配置文件：.env")

    print()
    print("=" * 60)

if __name__ == '__main__':
    main()
