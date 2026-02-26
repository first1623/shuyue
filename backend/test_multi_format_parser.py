#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多格式文档解析测试脚本
"""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# 显式加载 .env 文件
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# 添加 app 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from utils.document_parser import DocumentParser

def test_format(parser, file_path, file_id):
    """测试单个格式"""
    print(f"\n{'='*60}")
    print(f"测试文件: {file_path.name}")
    print(f"格式: {file_path.suffix.upper()}")
    print(f"{'='*60}")
    
    try:
        result = parser.parse_document(str(file_path), file_id)
        
        print(f"\n[成功] 解析成功！")
        print(f"状态: {result.get('status')}")
        print(f"词数: {result.get('word_count')}")
        print(f"置信度: {result.get('confidence_score')}")
        
        ai_analysis = result.get('deepseek_response', {})
        print(f"\nAI 分析结果:")
        print(f"  摘要: {ai_analysis.get('abstract', 'N/A')[:100]}...")
        print(f"  关键词: {ai_analysis.get('keywords', [])}")
        print(f"  理论/方法: {ai_analysis.get('theories', [])}")
        print(f"  结论: {ai_analysis.get('conclusion', 'N/A')[:100]}...")
        
        return True
    except Exception as e:
        print(f"\n[失败] 解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = DocumentParser()
    test_dir = Path("c:/Users/zhaoy/CodeBuddy/backend/data/test_documents")
    
    if not test_dir.exists():
        print(f"测试目录不存在: {test_dir}")
        print("请先运行 create_test_documents.py 创建测试文件")
        return
    
    # 测试所有支持的格式
    test_files = [
        ("test.md", 101),
        ("test.docx", 102),
        ("test.pdf", 103),  # 如果有 PDF 文件的话
    ]
    
    results = []
    for filename, file_id in test_files:
        file_path = test_dir / filename
        if file_path.exists():
            success = test_format(parser, file_path, file_id)
            results.append((filename, success))
        else:
            print(f"\n[跳过] 文件不存在: {filename}")
            results.append((filename, None))
    
    # 总结
    print(f"\n{'='*60}")
    print("测试总结")
    print(f"{'='*60}")
    for filename, success in results:
        if success is True:
            print(f"[成功] {filename}")
        elif success is False:
            print(f"[失败] {filename}")
        else:
            print(f"[跳过] {filename}")

if __name__ == "__main__":
    main()
