#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek 文档解析验证脚本
"""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# 显式加载 .env 文件（从 backend 目录）
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# 添加 app 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from utils.document_parser import DocumentParser

def main():
    parser = DocumentParser()
    
    # 测试文件路径（使用绝对路径避免工作目录问题）
    backend_dir = Path(__file__).parent
    test_file = backend_dir / "data" / "test.txt"
    if not test_file.exists():
        print(f"测试文件不存在: {test_file}")
        print("请确认文件已放置在 backend/data/test.txt")
        return
    
    # 假设 file_id 为 1
    file_id = 1
    
    try:
        print("开始解析文档并调用 DeepSeek API...")
        result = parser.parse_document(str(test_file), file_id)
        print("\n[成功] 解析成功！结果如下：\n")
        
        ai_analysis = result.get("deepseek_response", {})
        print("摘要:", ai_analysis.get("abstract"))
        print("关键词:", ai_analysis.get("keywords"))
        print("理论/方法:", ai_analysis.get("theories"))
        print("实验流程:", ai_analysis.get("experiment_flow"))
        print("统计方法:", ai_analysis.get("statistical_methods"))
        print("结论:", ai_analysis.get("conclusion"))
        print("置信度:", ai_analysis.get("confidence_score"))
        
    except Exception as e:
        print("[失败] 解析失败:", str(e))

if __name__ == "__main__":
    main()
