#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
用于创建数据库表结构
"""

import os
import sys

# 确保能找到 app 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from datetime import datetime

# ==================== 数据库配置 ====================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/knowledge_graph.db")

# 创建数据目录
os.makedirs("data", exist_ok=True)

print("=" * 60)
print("数据库初始化脚本")
print("=" * 60)
print(f"数据库路径: {DATABASE_URL}")
print()

# SQLAlchemy 配置
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=True
    )
    
    # 启用 SQLite 外键约束
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=True
    )

Base = declarative_base()


# ==================== 数据模型定义 ====================
class DataOverview(Base):
    """文件和文件夹信息表"""
    __tablename__ = "data_overview"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_name = Column(String(255), nullable=False, comment="文件名")
    file_path = Column(Text, nullable=False, unique=True, comment="完整路径")
    file_type = Column(String(50), nullable=False, comment="文件类型：folder/file")
    parent_id = Column(Integer, ForeignKey("data_overview.id", ondelete="CASCADE"), nullable=True, comment="父节点ID")
    
    file_size = Column(Integer, nullable=True, comment="文件大小（字节）")
    download_time = Column(DateTime, nullable=True, comment="下载时间")
    bookname = Column(String(500), nullable=True, comment="书籍文档名称")
    file_extension = Column(String(10), nullable=True, comment="文件扩展名")
    modified_time = Column(DateTime, nullable=True, comment="文件修改时间")
    is_deleted = Column(Boolean, default=False, comment="是否删除")
    doc_metadata = Column(JSON, nullable=True, comment="额外元数据")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DataBookDetail(Base):
    """文档详细信息表"""
    __tablename__ = "data_book_detail"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("data_overview.id", ondelete="CASCADE"), nullable=False, comment="关联data_overview表")
    
    abstract = Column(Text, nullable=True, comment="摘要信息")
    keywords = Column(JSON, nullable=True, comment="关键词列表")
    theories = Column(JSON, nullable=True, comment="引用的理论/参考文献")
    experiment_flow = Column(Text, nullable=True, comment="实验流程概述")
    statistical_methods = Column(JSON, nullable=True, comment="使用的统计方法")
    conclusion = Column(Text, nullable=True, comment="研究结论")
    full_text = Column(Text, nullable=True, comment="全文存储（可选）")
    
    # 三维度图谱字段
    authors = Column(JSON, nullable=True, comment="文档作者列表")
    theories_used = Column(JSON, nullable=True, comment="使用的理论/依据")
    entities = Column(JSON, nullable=True, comment="提取的实体词")
    entity_relations = Column(JSON, nullable=True, comment="实体间关系")
    
    # 解析状态
    parse_status = Column(String(20), default="pending", comment="解析状态：pending/processing/completed/failed")
    parse_time = Column(DateTime, nullable=True, comment="解析时间")
    parse_error = Column(Text, nullable=True, comment="解析错误信息")
    deepseek_response = Column(JSON, nullable=True, comment="DeepSeek API原始响应")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ==================== 初始化数据库 ====================
def init_database():
    """初始化数据库表结构"""
    print("正在创建数据库表...")
    
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        
        print()
        print("=" * 60)
        print("[OK] 数据库初始化成功！")
        print("=" * 60)
        print()
        print("已创建的表：")
        print("  - data_overview: 文件和文件夹信息表")
        print("  - data_book_detail: 文档详细信息表")
        print()
        print("数据库文件位置: data/knowledge_graph.db")
        print()
        print("下一步：")
        print("  1. 启动服务器: py minimal_server.py")
        print("  2. 访问 http://127.0.0.1:8000 查看API文档")
        print("  3. 调用 POST /api/v1/knowledge-tree/scan 扫描文件")
        print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print("[ERROR] 数据库初始化失败！")
        print("=" * 60)
        print(f"错误信息: {e}")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    init_database()
