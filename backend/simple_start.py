#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版启动脚本 - 避免复杂依赖问题
"""

import sys
import os
from pathlib import Path

def check_basic_requirements():
    """检查基本Python环境"""
    print("🔍 检查Python环境...")
    
    if sys.version_info < (3, 8):
        print("❌ 错误: 需要Python 3.8或更高版本")
        return False
    
    print(f"✅ Python版本: {sys.version}")
    return True

def check_config_file():
    """检查配置文件"""
    print("🔍 检查配置文件...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  警告: .env文件不存在，将使用默认配置")
        return True
    
    print("✅ 配置文件存在")
    return True

def check_imports():
    """检查关键模块导入"""
    print("🔍 检查模块导入...")
    
    # 测试基础导入
    try:
        import fastapi
        print("✅ FastAPI导入成功")
    except ImportError as e:
        print(f"❌ FastAPI导入失败: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn导入成功")
    except ImportError as e:
        print(f"❌ Uvicorn导入失败: {e}")
        return False
    
    # 测试项目模块导入
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from app.core.config import settings
        print("✅ 配置文件导入成功")
    except ImportError as e:
        print(f"❌ 配置文件导入失败: {e}")
        return False
    
    try:
        from app.core.database import engine, Base
        print("✅ 数据库模块导入成功")
    except ImportError as e:
        print(f"❌ 数据库模块导入失败: {e}")
        return False
    
    try:
        from app.views import knowledge_tree
        print("✅ 视图模块导入成功")
    except ImportError as e:
        print(f"❌ 视图模块导入失败: {e}")
        return False
    
    return True

def create_minimal_app():
    """创建最小化应用进行测试"""
    print("🔍 创建测试应用...")
    
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        app = FastAPI(title="测试应用")
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @app.get("/")
        def root():
            return {"message": "测试服务器运行成功!", "status": "ok"}
        
        @app.get("/health")
        def health():
            return {"status": "healthy"}
        
        print("✅ 测试应用创建成功")
        return app
        
    except Exception as e:
        print(f"❌ 测试应用创建失败: {e}")
        return None

def start_test_server():
    """启动测试服务器"""
    print("🚀 启动测试服务器...")
    
    try:
        import uvicorn
        app = create_minimal_app()
        
        if app:
            print("🌐 服务器将在 http://localhost:8000 运行")
            print("📚 API文档可在 http://localhost:8000/docs 查看")
            print("⏹️  按 Ctrl+C 停止服务器")
            
            uvicorn.run(
                app,
                host="127.0.0.1",
                port=8000,
                log_level="info"
            )
        else:
            return False
            
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
        return True
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        return False

def install_missing_deps():
    """提示安装缺失的依赖"""
    print("\n📦 安装Python依赖...")
    print("运行以下命令安装依赖:")
    print("pip install -r requirements-fixed.txt")
    
    choice = input("是否现在安装依赖? (y/n): ").lower().strip()
    
    if choice == 'y':
        try:
            import subprocess
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements-fixed.txt"
            ], capture_output=False)
            
            if result.returncode == 0:
                print("✅ 依赖安装成功")
                return True
            else:
                print("❌ 依赖安装失败")
                return False
        except Exception as e:
            print(f"❌ 安装过程出错: {e}")
            return False
    
    return False

def main():
    """主函数"""
    print("=== 学习平台知识图谱系统 - 启动诊断 ===")
    print()
    
    # 1. 检查Python环境
    if not check_basic_requirements():
        return 1
    
    print()
    
    # 2. 检查配置文件
    if not check_config_file():
        return 1
    
    print()
    
    # 3. 检查模块导入
    if not check_imports():
        print("\n🔧 检测到导入问题，可能需要安装依赖")
        if not install_missing_deps():
            print("请手动安装依赖后重试")
            return 1
        
        # 重新检查导入
        print("\n🔄 重新检查导入...")
        if not check_imports():
            print("❌ 导入仍有问题，请检查代码")
            return 1
    
    print()
    
    # 4. 启动测试服务器
    success = start_test_server()
    
    if success:
        print("✅ 程序运行成功!")
        return 0
    else:
        print("❌ 程序运行失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())