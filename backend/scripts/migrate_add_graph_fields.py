#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移脚本 - 添加三维度图谱字段
执行方式: python backend/scripts/migrate_add_graph_fields.py
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine, SessionLocal
from app.models.data_overview import DataBookDetail
from app.models.base import BaseModel

def migrate():
    """执行数据库迁移"""
    print("开始数据库迁移...")
    
    # 获取数据库连接
    db = SessionLocal()
    
    try:
        # 检查是否是SQLite
        if str(engine.url).startswith('sqlite'):
            print("检测到SQLite数据库，执行迁移...")
            
            # 检查表是否存在
            result = db.execute(text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='data_book_detail'"
            ))
            table_exists = result.fetchone() is not None
            
            if not table_exists:
                print("表 data_book_detail 不存在，创建新表...")
                # 创建所有表
                BaseModel.metadata.create_all(bind=engine)
                print("表创建成功")
            else:
                print("表 data_book_detail 已存在，检查新字段...")
                
                # 获取现有列
                result = db.execute(text("PRAGMA table_info(data_book_detail)"))
                existing_columns = {row[1] for row in result.fetchall()}
                
                print(f"现有列: {existing_columns}")
                
                # 新字段列表
                new_columns = ['authors', 'theories_used', 'entities', 'entity_relations']
                
                # 添加缺失的列
                for column in new_columns:
                    if column not in existing_columns:
                        print(f"添加列: {column}")
                        db.execute(text(f"ALTER TABLE data_book_detail ADD COLUMN {column} JSON"))
                        print(f"列 {column} 添加成功")
                    else:
                        print(f"列 {column} 已存在，跳过")
        else:
            # PostgreSQL
            print("检测到PostgreSQL数据库，执行迁移...")
            
            new_columns = [
                ('authors', 'JSON'),
                ('theories_used', 'JSON'),
                ('entities', 'JSON'),
                ('entity_relations', 'JSON')
            ]
            
            for column_name, column_type in new_columns:
                try:
                    db.execute(text(f"""
                        ALTER TABLE data_book_detail 
                        ADD COLUMN IF NOT EXISTS {column_name} {column_type}
                    """))
                    print(f"列 {column_name} 检查/添加完成")
                except Exception as e:
                    if "already exists" in str(e).lower() or "重复" in str(e):
                        print(f"列 {column_name} 已存在，跳过")
                    else:
                        raise
        
        db.commit()
        print("\n✅ 数据库迁移成功！")
        
        # 验证迁移结果
        print("\n验证迁移结果...")
        if str(engine.url).startswith('sqlite'):
            result = db.execute(text("PRAGMA table_info(data_book_detail)"))
            columns = [row[1] for row in result.fetchall()]
            print(f"当前表结构包含 {len(columns)} 个列")
            
            required_columns = ['authors', 'theories_used', 'entities', 'entity_relations']
            for col in required_columns:
                if col in columns:
                    print(f"  ✅ {col}")
                else:
                    print(f"  ❌ {col} 缺失")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ 迁移失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    migrate()
