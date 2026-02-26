#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库连接和基础设置
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from app.core.config import settings

# 尝试导入 Neo4j（可选依赖）
try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False
    print("警告: Neo4j 驱动未安装，图数据库功能将不可用")

# SQLAlchemy基础设置
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# 根据数据库类型调整参数
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    # SQLite 配置
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=settings.DEBUG
    )
    
    # 启用 SQLite 外键约束
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    
    print(f"使用 SQLite 数据库: {SQLALCHEMY_DATABASE_URL}")
else:
    # PostgreSQL 配置
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=settings.DEBUG
    )
    print(f"使用 PostgreSQL 数据库")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Neo4j连接（可选）
def get_neo4j_driver():
    """获取Neo4j驱动"""
    if not NEO4J_AVAILABLE:
        raise ImportError("Neo4j 驱动未安装，请运行: pip install neo4j")
    return GraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
    )

async def init_db():
    """初始化数据库连接"""
    try:
        from sqlalchemy import text
        
        # 测试数据库连接
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        db_type = "SQLite" if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else "PostgreSQL"
        print(f"{db_type}数据库连接成功")
        
        # 测试Neo4j连接（可选）
        if NEO4J_AVAILABLE:
            try:
                driver = get_neo4j_driver()
                with driver.session() as session:
                    session.run("RETURN 1")
                driver.close()
                print("Neo4j数据库连接成功")
            except Exception as e:
                print(f"Neo4j连接失败（可选功能）: {e}")
        
    except Exception as e:
        print(f"数据库连接失败: {e}")
        raise

@contextmanager
def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_neo4j_session():
    """获取Neo4j数据库会话"""
    if not NEO4J_AVAILABLE:
        raise ImportError("Neo4j 驱动未安装")
    driver = get_neo4j_driver()
    session = driver.session()
    try:
        yield session
    finally:
        session.close()
        driver.close()