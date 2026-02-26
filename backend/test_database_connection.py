#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库连接测试脚本
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

from sqlalchemy import text
from app.core.database import engine, Base
from app.core.config import settings

def test_database_connection():
    """测试数据库连接"""
    print("=" * 60)
    print("数据库连接测试")
    print("=" * 60)
    print(f"数据库 URL: {settings.DATABASE_URL}")
    print(f"主机: {settings.POSTGRES_HOST}")
    print(f"端口: {settings.POSTGRES_PORT}")
    print(f"用户: {settings.POSTGRES_USER}")
    print(f"数据库: {settings.POSTGRES_DB}")
    print("=" * 60)
    
    try:
        # 测试连接
        print("\n[测试 1] 尝试连接数据库...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("[成功] 数据库连接成功！")
        
        # 检查表是否存在
        print("\n[测试 2] 检查数据表...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result]
            if tables:
                print(f"[成功] 发现 {len(tables)} 个表: {', '.join(tables)}")
            else:
                print("[警告] 数据库中没有表，需要运行迁移创建表结构")
        
        return True
        
    except Exception as e:
        print(f"\n[失败] 数据库连接失败: {e}")
        print("\n可能的解决方案：")
        print("1. 确保 PostgreSQL 已安装并正在运行")
        print("2. 确保数据库 'knowledge_graph' 已创建")
        print("3. 检查 .env 文件中的数据库配置是否正确")
        print("4. 确保防火墙允许连接到端口 5432")
        return False

if __name__ == "__main__":
    test_database_connection()
