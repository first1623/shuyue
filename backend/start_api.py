#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动 FastAPI 服务器
"""
import sys
import os
from pathlib import Path
import uvicorn

# 添加项目根目录到路径
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# 加载环境变量
from dotenv import load_dotenv
env_path = backend_dir / ".env"
load_dotenv(env_path)

if __name__ == "__main__":
    print("=" * 60)
    print("学习平台知识图谱系统 API")
    print("=" * 60)
    print(f"服务地址: http://localhost:8001")
    print(f"API 文档: http://localhost:8001/docs")
    print(f"数据库: {os.getenv('DATABASE_URL', 'N/A')}")
    print("=" * 60)
    print("\n按 Ctrl+C 停止服务器\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        log_level="info"
    )
