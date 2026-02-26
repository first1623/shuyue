# -*- coding: utf-8 -*-
import sys
import io

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from config import Config

print("检查配置...")
try:
    Config.validate()
    print("[OK] 基础配置验证通过")
    api_key = Config.get_current_api_key()
    print(f"[OK] {Config.AI_PROVIDER.upper()} API Key: {api_key[:10]}...")
    print(f"[OK] 模型: {Config.get_current_model()}")
    print("\n配置检查通过！")
except Exception as e:
    print(f"[ERROR] 配置错误: {e}")

input("\n按回车键继续...")
