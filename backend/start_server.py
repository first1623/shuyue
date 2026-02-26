#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目启动脚本
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path

def check_dependencies():
    """检查必要的依赖"""
    print("检查项目依赖...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        return False
    
    # 检查配置文件
    env_file = Path(".env")
    if not env_file.exists():
        print("警告: .env文件不存在，将使用示例配置")
        if Path(".env.example").exists():
            env_file.write_text(Path(".env.example").read_text())
            print("已创建.env文件，请编辑配置后重新运行")
            return False
    
    return True

def install_requirements():
    """安装Python依赖"""
    print("安装Python依赖...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        return False

def init_database():
    """初始化数据库"""
    print("初始化数据库...")
    try:
        # 导入并运行数据库迁移
        from alembic import command
        from alembic.config import Config
        
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("数据库初始化完成")
        return True
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        print("请确保PostgreSQL和Neo4j服务正在运行")
        return False

def start_redis():
    """启动Redis服务（如果可用）"""
    print("检查Redis服务...")
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("Redis服务正常")
        return True
    except:
        print("警告: Redis服务不可用，某些功能可能受限")
        return False

def start_celery_worker():
    """启动Celery Worker"""
    print("启动Celery Worker...")
    def run_worker():
        subprocess.run([
            "celery", "-A", "app.tasks.celery_worker", "worker",
            "--loglevel=info", "--concurrency=2"
        ])
    
    worker_thread = threading.Thread(target=run_worker, daemon=True)
    worker_thread.start()
    time.sleep(3)  # 等待Worker启动
    print("Celery Worker已启动")

def start_server():
    """启动FastAPI服务器"""
    print("启动FastAPI服务器...")
    print("服务器将在 http://localhost:8000 运行")
    print("API文档可在 http://localhost:8000/api/docs 查看")
    
    try:
        subprocess.run([
            "uvicorn", "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n服务器已停止")

def main():
    """主函数"""
    print("=== 学习平台知识图谱系统 ===")
    print()
    
    # 检查依赖
    if not check_dependencies():
        return 1
    
    # 安装依赖
    if not install_requirements():
        return 1
    
    # 初始化数据库
    if not init_database():
        print("数据库初始化失败，但可以继续运行")
    
    # 检查Redis
    start_redis()
    
    # 启动Celery Worker
    try:
        start_celery_worker()
    except:
        print("Celery Worker启动失败，请手动启动: celery -A app.tasks.celery_worker worker --loglevel=info")
    
    print()
    print("所有服务准备就绪！")
    print()
    
    # 启动主服务器
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n程序已退出")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())