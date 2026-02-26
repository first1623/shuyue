#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证数据库保存的数据
"""
import sys
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# 显式加载 .env 文件
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# 添加 app 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.core.database import SessionLocal
from app.models.data_overview import DataBookDetail

def verify_saved_data():
    """验证数据库中保存的数据"""
    print("=" * 60)
    print("数据库数据验证")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        # 查询所有解析结果
        results = db.query(DataBookDetail).all()
        
        if not results:
            print("\n[提示] 数据库中没有保存的解析结果")
            return
        
        print(f"\n[成功] 找到 {len(results)} 条解析记录：\n")
        
        for i, record in enumerate(results, 1):
            print(f"--- 记录 {i} ---")
            print(f"文件 ID: {record.file_id}")
            print(f"解析状态: {record.parse_status}")
            print(f"解析时间: {record.parse_time}")
            print(f"摘要: {record.abstract}")
            print(f"关键词: {record.keywords}")
            print(f"理论/方法: {record.theories}")
            print(f"实验流程: {record.experiment_flow}")
            print(f"统计方法: {record.statistical_methods}")
            print(f"结论: {record.conclusion}")
            print(f"置信度: {record.deepseek_response.get('confidence_score') if record.deepseek_response else 'N/A'}")
            print(f"全文长度: {len(record.full_text) if record.full_text else 0} 字符")
            print()
            
    finally:
        db.close()

if __name__ == "__main__":
    verify_saved_data()
