#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 AI 调用"""

import sys
import os

if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("正在导入配置...")
from config import Config
print(f"AI Provider: {Config.AI_PROVIDER}")
print(f"API Key: {Config.DEEPSEEK_API_KEY[:20]}..." if Config.DEEPSEEK_API_KEY else "No API Key")

print("\n正在导入 AIClient...")
from ai_client import AIClient

print("\n正在初始化 AIClient...")
try:
    client = AIClient()
    print(f"初始化成功，模型: {client.model}")
except Exception as e:
    print(f"初始化失败: {e}")
    sys.exit(1)

print("\n正在测试简单对话...")
try:
    response = client.chat_completion([
        {"role": "user", "content": "你好，请回复'测试成功'"}
    ])
    print(f"响应类型: {type(response)}")
    
    # 提取内容
    if hasattr(response, 'choices'):
        content = response.choices[0].message.content
        print(f"AI 回复: {content}")
    else:
        print(f"响应: {response}")
        
    print("\n测试成功！")
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()
