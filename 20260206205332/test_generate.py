#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试文章生成流程"""

import sys
import os

if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("开始测试文章生成...")
print("=" * 60)

try:
    from wechat_main import WeChatContentSystem
    
    print("\n1. 初始化系统...")
    system = WeChatContentSystem()
    print("系统初始化成功")
    
    print("\n2. 开始生成文章...")
    theme = "小朋友总是发脾气，你可以这么做"
    print(f"主题: {theme}")
    
    print("\n3. 调用 process_theme...")
    content_package = system.process_theme(theme)
    
    print("\n4. 生成完成!")
    print("=" * 60)
    print(f"标题: {content_package['article']['title']}")
    print(f"摘要: {content_package['article']['digest'][:50]}...")
    print(f"内容长度: {len(content_package['article']['content'])} 字符")
    print("=" * 60)
    
except Exception as e:
    print(f"\n测试失败: {e}")
    import traceback
    traceback.print_exc()
