#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简版服务器 - 专为Python 3.13设计，避免编译依赖
支持数据库持久化存储（PostgreSQL/SQLite）
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List
from collections import defaultdict

# 数据库相关导入
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from contextlib import contextmanager

# ==================== 数据库配置 ====================
# 默认使用 SQLite，方便部署；可通过环境变量切换到 PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/knowledge_graph.db")

# 创建数据目录
os.makedirs("data", exist_ok=True)

# SQLAlchemy 配置
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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
    
    # 关系
    children = relationship("DataOverview", backref="parent", remote_side=[id])
    book_detail = relationship("DataBookDetail", back_populates="file_info", uselist=False)


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
    
    # 关系
    file_info = relationship("DataOverview", back_populates="book_detail")


# 创建所有表
Base.metadata.create_all(bind=engine)


# ==================== 数据库会话管理 ====================
@contextmanager
def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session():
    """FastAPI 依赖注入用"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建FastAPI应用
app = FastAPI(
    title="学习平台知识图谱系统",
    description="极简版 - Python 3.13兼容，支持数据库持久化",
    version="2.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 扫描状态存储
scan_status_store: Dict[str, Any] = {
    "status": "idle",
    "progress": 0,
    "current_file": "",
    "current_path": "",
    "total_files": 0,
    "scanned_files": 0,
    "total_folders": 0,
    "start_time": None,
    "errors": [],
    "files": [],
    "folders": []
}

# 支持的文件类型
SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.txt', '.md', '.pptx', '.xlsx', '.xls'}

# 存储扫描后的真实数据
scanned_files_store: Dict[str, Any] = {
    "files": [],
    "folders": [],
    "tree": [],
    "stats": {
        "total_files": 0,
        "total_folders": 0,
        "supported_docs": 0,
        "total_size_mb": 0.0
    }
}

# 模拟数据（避免数据库依赖）- 仅作为备用
mock_stats = {
    "total_files": 1247,
    "total_folders": 156,
    "supported_docs": 892,
    "total_size_mb": 2847.5,
    "parse_success_rate": 94.2,
    "active_users": 23
}

mock_tree = [
    {
        "id": 1,
        "name": "知识库根目录",
        "path": "D:/zyfdownloadanalysis",
        "type": "folder",
        "children": [
            {
                "id": 2,
                "name": "机器学习教程",
                "path": "D:/zyfdownloadanalysis/machine-learning",
                "type": "folder",
                "children": [
                    {
                        "id": 3,
                        "name": "深度学习基础.pdf",
                        "path": "D:/zyfdownloadanalysis/machine-learning/deep-learning.pdf",
                        "type": "file",
                        "size": 2048576,
                        "extension": ".pdf"
                    },
                    {
                        "id": 4,
                        "name": "神经网络原理.docx",
                        "path": "D:/zyfdownloadanalysis/machine-learning/neural-networks.docx",
                        "type": "file",
                        "size": 1536000,
                        "extension": ".docx"
                    }
                ]
            },
            {
                "id": 5,
                "name": "编程资料",
                "path": "D:/zyfdownloadanalysis/programming",
                "type": "folder",
                "children": [
                    {
                        "id": 6,
                        "name": "Python进阶.md",
                        "path": "D:/zyfdownloadanalysis/programming/python-advanced.md",
                        "type": "file",
                        "size": 51200,
                        "extension": ".md"
                    }
                ]
            }
        ]
    }
]


def build_tree_from_files(files: list, folders: list, root_path: str) -> list:
    """从文件列表构建树形结构"""
    if not files and not folders:
        return []
    
    # 创建路径到节点的映射
    path_to_node: Dict[str, Any] = {}
    all_paths = set()
    
    # 首先添加所有文件夹
    for folder in folders:
        path = folder["path"].replace("\\", "/")
        all_paths.add(path)
        path_to_node[path] = {
            "id": folder["id"],
            "name": folder["name"],
            "path": path,
            "type": "folder",
            "children": []
        }
    
    # 添加所有文件
    for file in files:
        path = file["path"].replace("\\", "/")
        dir_path = os.path.dirname(path).replace("\\", "/")
        all_paths.add(dir_path)
        
        # 确保父目录存在
        if dir_path not in path_to_node:
            path_to_node[dir_path] = {
                "id": len(path_to_node) + 10000,
                "name": os.path.basename(dir_path) or dir_path,
                "path": dir_path,
                "type": "folder",
                "children": []
            }
        
        # 添加文件节点
        file_node = {
            "id": file["id"],
            "name": file["name"],
            "path": path,
            "type": "file",
            "size": file.get("size", 0),
            "extension": file.get("extension", ""),
        }
        path_to_node[dir_path]["children"].append(file_node)
    
    # 构建父子关系
    root_nodes = []
    sorted_paths = sorted(all_paths, key=lambda x: x.count("/"))
    
    for path in sorted_paths:
        node = path_to_node.get(path)
        if not node:
            continue
            
        parent_path = os.path.dirname(path).replace("\\", "/")
        
        # 如果是根目录或父目录不存在，作为根节点
        if not parent_path or parent_path not in path_to_node:
            root_nodes.append(node)
        elif parent_path != path:
            # 添加到父节点
            parent_node = path_to_node.get(parent_path)
            if parent_node and node not in parent_node.get("children", []):
                # 避免重复添加
                existing_ids = {c.get("id") for c in parent_node.get("children", [])}
                if node["id"] not in existing_ids:
                    parent_node.setdefault("children", []).append(node)
    
    return root_nodes if root_nodes else [path_to_node.get(root_path.replace("\\", "/"), {})]

# 根路径 - 健康检查
@app.get("/")
async def root():
    return {
        "message": "学习平台知识图谱系统API服务",
        "version": "1.0.0",
        "status": "running",
        "python_version": "3.13",
        "mode": "minimal_compatible"
    }

# 健康检查
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "knowledge_graph_api",
        "timestamp": datetime.now().isoformat(),
        "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}"
    }

# 系统统计（从数据库读取）
@app.get("/api/v1/system/stats")
async def get_system_stats(db: Session = Depends(get_db_session)):
    """获取系统统计信息 - 从数据库读取"""
    try:
        # 统计文件和文件夹数量
        total_files = db.query(DataOverview).filter(
            DataOverview.file_type == "file",
            DataOverview.is_deleted == False
        ).count()
        
        total_folders = db.query(DataOverview).filter(
            DataOverview.file_type == "folder",
            DataOverview.is_deleted == False
        ).count()
        
        # 统计支持的文档数量
        supported_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md', '.pptx', '.xlsx', '.xls']
        supported_docs = db.query(DataOverview).filter(
            DataOverview.file_type == "file",
            DataOverview.file_extension.in_(supported_extensions),
            DataOverview.is_deleted == False
        ).count()
        
        # 统计总大小
        from sqlalchemy import func
        total_size_result = db.query(func.sum(DataOverview.file_size)).filter(
            DataOverview.file_type == "file",
            DataOverview.is_deleted == False
        ).scalar()
        total_size_mb = round((total_size_result or 0) / (1024 * 1024), 2)
        
        # 统计解析成功率
        completed_parses = db.query(DataBookDetail).filter(
            DataBookDetail.parse_status == "completed"
        ).count()
        total_parses = db.query(DataBookDetail).count()
        parse_success_rate = round((completed_parses / total_parses * 100), 1) if total_parses > 0 else 0
        
        return {
            "code": 200,
            "message": "success",
            "data": {
                "total_files": total_files,
                "total_folders": total_folders,
                "supported_docs": supported_docs,
                "total_size_mb": total_size_mb,
                "parse_success_rate": parse_success_rate,
                "active_users": 1  # 单用户系统
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "code": 200,
            "message": "success",
            "data": mock_stats,
            "timestamp": datetime.now().isoformat()
        }


# 数据库初始化端点
@app.post("/api/v1/database/init")
async def init_database():
    """初始化数据库表结构"""
    try:
        Base.metadata.create_all(bind=engine)
        return {
            "code": 200,
            "message": "数据库初始化成功",
            "data": {
                "database_url": DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else DATABASE_URL,
                "tables": ["data_overview", "data_book_detail"]
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"数据库初始化失败: {str(e)}",
            "data": None,
            "timestamp": datetime.now().isoformat()
        }


# 数据库状态检查
@app.get("/api/v1/database/status")
async def check_database_status(db: Session = Depends(get_db_session)):
    """检查数据库连接状态"""
    try:
        from sqlalchemy import text
        
        # 执行简单查询测试连接
        db.execute(text("SELECT 1"))
        
        # 获取表统计信息
        file_count = db.query(DataOverview).filter(DataOverview.file_type == "file").count()
        folder_count = db.query(DataOverview).filter(DataOverview.file_type == "folder").count()
        detail_count = db.query(DataBookDetail).count()
        
        return {
            "code": 200,
            "message": "数据库连接正常",
            "data": {
                "status": "connected",
                "database_type": "SQLite" if DATABASE_URL.startswith("sqlite") else "PostgreSQL",
                "tables": {
                    "data_overview": {
                        "files": file_count,
                        "folders": folder_count,
                        "total": file_count + folder_count
                    },
                    "data_book_detail": {
                        "total": detail_count
                    }
                }
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"数据库连接失败: {str(e)}",
            "data": {"status": "disconnected"},
            "timestamp": datetime.now().isoformat()
        }

# 后台扫描任务
async def scan_folder_task(folder_path: str):
    """后台扫描文件夹任务 - 将数据存入数据库"""
    global scan_status_store, scanned_files_store
    
    scan_status_store = {
        "status": "processing",
        "progress": 0,
        "current_file": "",
        "current_path": folder_path,
        "total_files": 0,
        "scanned_files": 0,
        "total_folders": 0,
        "start_time": datetime.now().isoformat(),
        "errors": [],
        "files": [],
        "folders": []
    }
    
    # 重置扫描数据存储（用于前端实时展示）
    scanned_files_store = {
        "files": [],
        "folders": [],
        "tree": [],
        "stats": {
            "total_files": 0,
            "total_folders": 0,
            "supported_docs": 0,
            "total_size_mb": 0.0
        }
    }
    
    # 先统计文件总数
    try:
        for root, dirs, files in os.walk(folder_path):
            scan_status_store["total_folders"] += len(dirs)
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in SUPPORTED_EXTENSIONS:
                    scan_status_store["total_files"] += 1
    except Exception as e:
        scan_status_store["errors"].append(str(e))
        scan_status_store["status"] = "error"
        return
    
    if scan_status_store["total_files"] == 0:
        scan_status_store["status"] = "completed"
        scan_status_store["progress"] = 100
        scanned_files_store["tree"] = [{
            "id": 1,
            "name": os.path.basename(folder_path) or folder_path,
            "path": folder_path,
            "type": "folder",
            "children": []
        }]
        return
    
    # 扫描文件并存入数据库
    total_size = 0
    added_folders = {}  # 路径 -> 数据库ID映射
    
    try:
        with get_db() as db:
            # 创建根目录节点
            root_normalized = folder_path.replace("\\", "/")
            root_folder = db.query(DataOverview).filter(
                DataOverview.file_path == root_normalized
            ).first()
            
            if not root_folder:
                root_folder = DataOverview(
                    file_name=os.path.basename(folder_path) or folder_path,
                    file_path=root_normalized,
                    file_type="folder",
                    parent_id=None
                )
                db.add(root_folder)
                db.commit()
                db.refresh(root_folder)
            
            added_folders[root_normalized] = root_folder.id
            
            # 遍历所有文件和文件夹
            for root, dirs, files in os.walk(folder_path):
                root_normalized = root.replace("\\", "/")
                
                # 确保当前目录在数据库中
                if root_normalized not in added_folders:
                    parent_path = os.path.dirname(root_normalized).replace("\\", "/")
                    parent_id = added_folders.get(parent_path)
                    
                    current_folder = DataOverview(
                        file_name=os.path.basename(root) or root,
                        file_path=root_normalized,
                        file_type="folder",
                        parent_id=parent_id
                    )
                    db.add(current_folder)
                    db.commit()
                    db.refresh(current_folder)
                    added_folders[root_normalized] = current_folder.id
                    
                    # 更新状态
                    scan_status_store["folders"].append({
                        "id": current_folder.id,
                        "name": current_folder.file_name,
                        "path": current_folder.file_path,
                        "type": "folder"
                    })
                
                # 处理文件
                parent_id = added_folders[root_normalized]
                
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in SUPPORTED_EXTENSIONS:
                        file_path = os.path.join(root, file)
                        file_path_normalized = file_path.replace("\\", "/")
                        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
                        total_size += file_size
                        
                        # 更新状态
                        scan_status_store["current_file"] = file
                        scan_status_store["current_path"] = root
                        scan_status_store["scanned_files"] += 1
                        scan_status_store["progress"] = int(
                            (scan_status_store["scanned_files"] / scan_status_store["total_files"]) * 100
                        )
                        
                        # 检查文件是否已存在
                        existing_file = db.query(DataOverview).filter(
                            DataOverview.file_path == file_path_normalized
                        ).first()
                        
                        if existing_file:
                            file_info = {
                                "id": existing_file.id,
                                "name": existing_file.file_name,
                                "path": existing_file.file_path,
                                "type": "file",
                                "file_type": ext.replace('.', ''),
                                "size": existing_file.file_size or file_size,
                                "extension": ext,
                                "parse_status": "pending",
                                "created_at": existing_file.created_at.strftime("%Y-%m-%d %H:%M:%S") if existing_file.created_at else "",
                                "updated_at": existing_file.updated_at.strftime("%Y-%m-%d %H:%M:%S") if existing_file.updated_at else ""
                            }
                        else:
                            # 创建新文件记录
                            new_file = DataOverview(
                                file_name=file,
                                file_path=file_path_normalized,
                                file_type="file",
                                parent_id=parent_id,
                                file_size=file_size,
                                file_extension=ext,
                                modified_time=datetime.fromtimestamp(os.path.getmtime(file_path)) if os.path.exists(file_path) else None
                            )
                            db.add(new_file)
                            db.commit()
                            db.refresh(new_file)
                            
                            # 创建对应的解析记录
                            existing_detail = db.query(DataBookDetail).filter(
                                DataBookDetail.file_id == new_file.id
                            ).first()
                            if not existing_detail:
                                new_detail = DataBookDetail(
                                    file_id=new_file.id,
                                    parse_status="pending"
                                )
                                db.add(new_detail)
                                db.commit()
                            
                            file_info = {
                                "id": new_file.id,
                                "name": file,
                                "path": file_path_normalized,
                                "type": "file",
                                "file_type": ext.replace('.', ''),
                                "size": file_size,
                                "extension": ext,
                                "parse_status": "pending",
                                "created_at": new_file.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_at": new_file.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                            }
                        
                        scan_status_store["files"].append(file_info)
                        scanned_files_store["files"].append(file_info)
                        
                        await asyncio.sleep(0.01)
                        
    except Exception as e:
        scan_status_store["errors"].append(str(e))
        print(f"扫描错误: {e}")
        import traceback
        traceback.print_exc()
    
    # 构建树形结构（用于前端展示）
    scanned_files_store["folders"] = scan_status_store["folders"]
    scanned_files_store["tree"] = build_tree_from_files(
        scan_status_store["files"],
        scan_status_store["folders"],
        folder_path
    )
    
    # 更新统计信息
    scanned_files_store["stats"] = {
        "total_files": scan_status_store["scanned_files"],
        "total_folders": len(scan_status_store["folders"]),
        "supported_docs": scan_status_store["scanned_files"],
        "total_size_mb": round(total_size / (1024 * 1024), 2)
    }
    
    # 完成
    scan_status_store["status"] = "completed"
    scan_status_store["progress"] = 100
    scan_status_store["current_file"] = ""

# 知识树扫描
@app.post("/api/v1/knowledge-tree/scan")
async def scan_knowledge_tree(background_tasks: BackgroundTasks, folder_path: str = "D:/zyfdownloadanalysis"):
    # 重置状态
    global scan_status_store
    scan_status_store["status"] = "processing"
    scan_status_store["progress"] = 0
    scan_status_store["start_time"] = datetime.now().isoformat()
    
    # 启动后台任务
    background_tasks.add_task(scan_folder_task, folder_path)
    
    return {
        "code": 200,
        "message": "扫描任务已开始",
        "data": {
            "task_id": "scan_task_001",
            "status": "processing",
            "folder_path": folder_path
        },
        "timestamp": datetime.now().isoformat()
    }

# 扫描进度查询
@app.get("/api/v1/knowledge-tree/scan/status")
async def get_scan_status():
    return {
        "code": 200,
        "message": "success",
        "data": scan_status_store,
        "timestamp": datetime.now().isoformat()
    }

# 获取知识树（从数据库读取）
@app.get("/api/v1/knowledge-tree")
async def get_knowledge_tree(db: Session = Depends(get_db_session)):
    """获取知识树 - 从数据库读取"""
    try:
        # 从数据库获取所有文件和文件夹
        files_db = db.query(DataOverview).filter(
            DataOverview.is_deleted == False
        ).order_by(DataOverview.file_path).all()
        
        if files_db:
            # 构建树形结构
            files = []
            folders = []
            
            for item in files_db:
                if item.file_type == "file":
                    detail = db.query(DataBookDetail).filter(DataBookDetail.file_id == item.id).first()
                    files.append({
                        "id": item.id,
                        "name": item.file_name,
                        "path": item.file_path,
                        "type": "file",
                        "size": item.file_size or 0,
                        "extension": item.file_extension or "",
                        "parse_status": detail.parse_status if detail else "pending"
                    })
                else:
                    folders.append({
                        "id": item.id,
                        "name": item.file_name,
                        "path": item.file_path,
                        "type": "folder",
                        "parent_id": item.parent_id
                    })
            
            # 构建树
            tree = build_tree_from_files(files, folders, folders[0]["path"] if folders else "")
            
            # 统计信息
            stats = {
                "total_files": len(files),
                "total_folders": len(folders),
                "supported_docs": len(files),
                "total_size_mb": round(sum(f["size"] for f in files) / (1024 * 1024), 2)
            }
            
            return {
                "code": 200,
                "message": "success",
                "data": tree,
                "stats": stats,
                "timestamp": datetime.now().isoformat()
            }
        
        # 如果数据库为空，返回模拟数据
        return {
            "code": 200,
            "message": "success",
            "data": mock_tree,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "code": 200,
            "message": "success",
            "data": mock_tree,
            "timestamp": datetime.now().isoformat()
        }

# 获取已扫描的文件列表（从数据库读取）
@app.get("/api/v1/knowledge-tree/scanned-files")
async def get_scanned_files(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    """获取已扫描的文件列表 - 从数据库读取"""
    try:
        # 从数据库获取文件
        files_query = db.query(DataOverview).filter(
            DataOverview.file_type == "file",
            DataOverview.is_deleted == False
        ).order_by(DataOverview.id)
        
        total_files = files_query.count()
        files_db = files_query.offset(skip).limit(limit).all()
        
        # 从数据库获取文件夹
        folders_db = db.query(DataOverview).filter(
            DataOverview.file_type == "folder",
            DataOverview.is_deleted == False
        ).limit(50).all()
        
        # 格式化返回数据
        files = []
        for f in files_db:
            # 获取解析状态
            detail = db.query(DataBookDetail).filter(DataBookDetail.file_id == f.id).first()
            parse_status = detail.parse_status if detail else "pending"
            
            files.append({
                "id": f.id,
                "name": f.file_name,
                "path": f.file_path,
                "type": "file",
                "file_type": f.file_extension.replace('.', '') if f.file_extension else "",
                "size": f.file_size or 0,
                "extension": f.file_extension or "",
                "parse_status": parse_status,
                "created_at": f.created_at.strftime("%Y-%m-%d %H:%M:%S") if f.created_at else "",
                "updated_at": f.updated_at.strftime("%Y-%m-%d %H:%M:%S") if f.updated_at else ""
            })
        
        folders = [{
            "id": f.id,
            "name": f.file_name,
            "path": f.file_path,
            "type": "folder"
        } for f in folders_db]
        
        return {
            "code": 200,
            "message": "success",
            "data": {
                "files": files,
                "folders": folders,
                "total_files": total_files,
                "total_folders": db.query(DataOverview).filter(
                    DataOverview.file_type == "folder",
                    DataOverview.is_deleted == False
                ).count()
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取文件列表失败: {str(e)}",
            "data": None,
            "timestamp": datetime.now().isoformat()
        }

# 预览文件内容（从数据库读取）
@app.get("/api/v1/knowledge-tree/files/{file_id}/preview")
async def preview_file(file_id: int, db: Session = Depends(get_db_session)):
    """预览文件内容 - 从数据库读取"""
    try:
        # 从数据库获取文件
        file_record = db.query(DataOverview).filter(DataOverview.id == file_id).first()
        
        if not file_record:
            return {
                "code": 404,
                "message": "文件不存在",
                "data": None,
                "timestamp": datetime.now().isoformat()
            }
        
        # 获取解析详情
        detail = db.query(DataBookDetail).filter(DataBookDetail.file_id == file_id).first()
        parse_status = detail.parse_status if detail else "pending"
        
        # 读取内容
        content = "暂无解析内容"
        try:
            text_extensions = ['.txt', '.md', '.json', '.csv', '.xml', '.html', '.css', '.js', '.py']
            if file_record.file_extension and file_record.file_extension.lower() in text_extensions:
                if os.path.exists(file_record.file_path):
                    with open(file_record.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(10000)
            elif detail and detail.abstract:
                # 如果有解析结果，显示摘要
                content = f"【文档摘要】\n{detail.abstract}\n\n"
                if detail.keywords:
                    content += f"【关键词】\n{', '.join(detail.keywords)}\n\n"
                if detail.authors:
                    content += f"【作者】\n{', '.join(detail.authors)}\n"
            else:
                content = f"文件类型 {file_record.file_extension or '未知'} 暂不支持预览，请先解析文档"
        except Exception as e:
            content = f"读取文件失败: {str(e)}"
        
        return {
            "code": 200,
            "message": "success",
            "data": {
                "id": file_record.id,
                "name": file_record.file_name,
                "path": file_record.file_path,
                "extension": file_record.file_extension or "",
                "size": file_record.file_size or 0,
                "parse_status": parse_status,
                "content": content,
                "abstract": detail.abstract if detail else None,
                "keywords": detail.keywords if detail else []
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"预览文件失败: {str(e)}",
            "data": None,
            "timestamp": datetime.now().isoformat()
        }

# 文档解析
@app.post("/api/v1/documents/{doc_id}/parse")
async def parse_document(doc_id: int):
    return {
        "code": 200,
        "message": "解析任务已开始",
        "data": {
            "task_id": f"parse_task_{doc_id}",
            "status": "processing",
            "estimated_time": "2分钟"
        },
        "timestamp": datetime.now().isoformat()
    }

# 获取文档列表（从数据库读取）
@app.get("/api/v1/documents")
async def get_documents(skip: int = 0, limit: int = 20, file_type: str = None, db: Session = Depends(get_db_session)):
    """获取文档列表 - 从数据库读取"""
    try:
        # 构建查询
        query = db.query(DataOverview).filter(
            DataOverview.file_type == "file",
            DataOverview.is_deleted == False
        )
        
        # 按文件类型过滤
        if file_type:
            query = query.filter(DataOverview.file_extension == f".{file_type}")
        
        # 获取总数
        total = query.count()
        
        # 分页获取
        documents_db = query.order_by(DataOverview.updated_at.desc()).offset(skip).limit(limit).all()
        
        # 格式化返回数据
        documents = []
        for doc in documents_db:
            # 获取解析状态
            detail = db.query(DataBookDetail).filter(DataBookDetail.file_id == doc.id).first()
            parse_status = detail.parse_status if detail else "pending"
            
            documents.append({
                "id": doc.id,
                "name": doc.file_name,
                "path": doc.file_path,
                "type": "file",
                "file_type": doc.file_extension.replace('.', '') if doc.file_extension else "",
                "size": doc.file_size or 0,
                "extension": doc.file_extension or "",
                "parse_status": parse_status,
                "created_at": doc.created_at.strftime("%Y-%m-%d %H:%M:%S") if doc.created_at else "",
                "updated_at": doc.updated_at.strftime("%Y-%m-%d %H:%M:%S") if doc.updated_at else ""
            })
        
        return {
            "code": 200,
            "message": "success",
            "data": {
                "documents": documents,
                "total": total,
                "skip": skip,
                "limit": limit
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取文档列表失败: {str(e)}",
            "data": None,
            "timestamp": datetime.now().isoformat()
        }

# 获取文档详情（从数据库读取）
@app.get("/api/v1/documents/{document_id}")
async def get_document_detail(document_id: int, db: Session = Depends(get_db_session)):
    """获取文档详情 - 从数据库读取"""
    try:
        # 从数据库获取文件信息
        doc = db.query(DataOverview).filter(DataOverview.id == document_id).first()
        
        if not doc:
            return {
                "code": 404,
                "message": "文档不存在",
                "data": None,
                "timestamp": datetime.now().isoformat()
            }
        
        # 获取解析详情
        detail = db.query(DataBookDetail).filter(DataBookDetail.file_id == document_id).first()
        
        # 构建返回数据
        result = {
            "id": doc.id,
            "name": doc.file_name,
            "path": doc.file_path,
            "type": "file",
            "size": doc.file_size or 0,
            "extension": doc.file_extension or "",
            "bookname": os.path.splitext(doc.file_name)[0],
            "parse_status": detail.parse_status if detail else "pending",
            "keywords": detail.keywords if detail and detail.keywords else [],
            "abstract": detail.abstract if detail else "",
            "created_at": doc.created_at.strftime("%Y-%m-%d %H:%M:%S") if doc.created_at else "",
            "updated_at": doc.updated_at.strftime("%Y-%m-%d %H:%M:%S") if doc.updated_at else ""
        }
        
        # 如果有详细信息，添加更多字段
        if detail:
            result.update({
                "authors": detail.authors or [],
                "theories": detail.theories or [],
                "theories_used": detail.theories_used or [],
                "entities": detail.entities or [],
                "entity_relations": detail.entity_relations or [],
                "experiment_flow": detail.experiment_flow,
                "statistical_methods": detail.statistical_methods or [],
                "conclusion": detail.conclusion
            })
        
        return {
            "code": 200,
            "message": "success",
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取文档详情失败: {str(e)}",
            "data": None,
            "timestamp": datetime.now().isoformat()
        }

# 解析文档（通用接口）- 状态持久化
@app.post("/api/v1/documents/parse")
async def parse_document_general(request: dict, background_tasks: BackgroundTasks, db: Session = Depends(get_db_session)):
    """解析文档 - 调用真正的 DocumentParser 和 DeepSeek API，状态持久化到数据库"""
    file_path = request.get("file_path")
    file_id = request.get("file_id")
    force_reparse = request.get("force_reparse", False)  # 强制重新解析
    
    if not file_path or not file_id:
        return {
            "code": 400,
            "message": "缺少必要参数: file_path 或 file_id",
            "data": None,
            "timestamp": datetime.now().isoformat()
        }
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return {
            "code": 404,
            "message": f"文件不存在: {file_path}",
            "data": None,
            "timestamp": datetime.now().isoformat()
        }
    
    # 检查当前解析状态
    detail = db.query(DataBookDetail).filter(DataBookDetail.file_id == int(file_id)).first()
    current_status = detail.parse_status if detail else "pending"
    previous_parse_time = detail.parse_time if detail else None
    
    # 若文档已解析且未强制重新解析，返回当前状态
    if current_status == "completed" and not force_reparse:
        return {
            "code": 200,
            "message": "文档已解析完成",
            "data": {
                "task_id": f"parse_task_{file_id}",
                "file_id": file_id,
                "file_path": file_path,
                "status": "completed",
                "parse_time": previous_parse_time.strftime("%Y-%m-%d %H:%M:%S") if previous_parse_time else None,
                "note": "文档已解析完成，如需重新解析请设置 force_reparse=true"
            },
            "timestamp": datetime.now().isoformat()
        }
    
    # 若文档正在解析中，返回当前状态
    if current_status == "processing":
        return {
            "code": 200,
            "message": "文档正在解析中",
            "data": {
                "task_id": f"parse_task_{file_id}",
                "file_id": file_id,
                "file_path": file_path,
                "status": "processing",
                "note": "文档正在解析中，请稍后再查询"
            },
            "timestamp": datetime.now().isoformat()
        }
    
    # 更新数据库状态为 processing（正在解析）
    try:
        if not detail:
            # 创建新的解析记录
            detail = DataBookDetail(
                file_id=int(file_id),
                parse_status="processing"
            )
            db.add(detail)
        else:
            # 更新已有记录
            detail.parse_status = "processing"
            detail.parse_error = None  # 清除之前的错误
        db.commit()
        print(f"[解析状态] 文件 {file_id} 开始解析，状态: processing")
    except Exception as e:
        print(f"更新解析状态失败: {e}")
    
    # 后台执行解析任务
    def run_parse_task():
        try:
            from app.utils.document_parser import DocumentParser
            parser = DocumentParser()
            
            # 更新解析进度
            with get_db() as db_session:
                detail = db_session.query(DataBookDetail).filter(
                    DataBookDetail.file_id == int(file_id)
                ).first()
                if detail:
                    detail.parse_status = "processing"
                    db_session.commit()
            
            print(f"[DeepSeek解析] 开始解析: {file_path}")
            
            result = parser.parse_document(file_path, int(file_id))
            print(f"[DeepSeek解析] 完成: {file_path}")
            print(f"[缓存统计] {parser.get_stats()}")
            
            # 更新数据库状态为 completed（解析完成）
            with get_db() as db_session:
                detail = db_session.query(DataBookDetail).filter(
                    DataBookDetail.file_id == int(file_id)
                ).first()
                if detail:
                    detail.parse_status = "completed"
                    detail.parse_time = datetime.utcnow()
                    detail.parse_error = None
                    db_session.commit()
                    print(f"[解析状态] 文件 {file_id} 解析完成，状态: completed")
                    
        except Exception as e:
            print(f"[DeepSeek解析] 失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 更新数据库状态为 failed（解析失败）
            try:
                with get_db() as db_session:
                    detail = db_session.query(DataBookDetail).filter(
                        DataBookDetail.file_id == int(file_id)
                    ).first()
                    if detail:
                        detail.parse_status = "failed"
                        detail.parse_error = str(e)
                        detail.parse_time = datetime.utcnow()
                        db_session.commit()
                        print(f"[解析状态] 文件 {file_id} 解析失败，状态: failed")
            except:
                pass
    
    background_tasks.add_task(run_parse_task)
    
    # 返回解析任务信息
    message = "重新解析任务已开始" if current_status == "completed" else "解析任务已开始"
    
    return {
        "code": 200,
        "message": message,
        "data": {
            "task_id": f"parse_task_{file_id}",
            "file_id": file_id,
            "file_path": file_path,
            "status": "processing",
            "previous_status": current_status,
            "estimated_time": "2-5分钟",
            "note": "解析完成后状态将更新为 completed"
        },
        "timestamp": datetime.now().isoformat()
    }


# 获取文档解析状态
@app.get("/api/v1/documents/{document_id}/parse/status")
async def get_parse_status(document_id: int, db: Session = Depends(get_db_session)):
    """获取文档解析状态"""
    try:
        detail = db.query(DataBookDetail).filter(DataBookDetail.file_id == document_id).first()
        
        if not detail:
            return {
                "code": 404,
                "message": "解析记录不存在",
                "data": {
                    "file_id": document_id,
                    "parse_status": "pending",
                    "parse_time": None,
                    "parse_error": None
                },
                "timestamp": datetime.now().isoformat()
            }
        
        return {
            "code": 200,
            "message": "success",
            "data": {
                "file_id": detail.file_id,
                "parse_status": detail.parse_status,
                "parse_time": detail.parse_time.strftime("%Y-%m-%d %H:%M:%S") if detail.parse_time else None,
                "parse_error": detail.parse_error,
                "has_keywords": bool(detail.keywords),
                "has_abstract": bool(detail.abstract),
                "has_entities": bool(detail.entities)
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取解析状态失败: {str(e)}",
            "data": None,
            "timestamp": datetime.now().isoformat()
        }


# 批量获取解析状态
@app.post("/api/v1/documents/parse/status/batch")
async def get_batch_parse_status(request: dict, db: Session = Depends(get_db_session)):
    """批量获取文档解析状态"""
    file_ids = request.get("file_ids", [])
    
    if not file_ids:
        return {
            "code": 400,
            "message": "缺少 file_ids 参数",
            "data": [],
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        details = db.query(DataBookDetail).filter(
            DataBookDetail.file_id.in_(file_ids)
        ).all()
        
        # 构建结果映射
        result_map = {}
        for detail in details:
            result_map[detail.file_id] = {
                "file_id": detail.file_id,
                "parse_status": detail.parse_status,
                "parse_time": detail.parse_time.strftime("%Y-%m-%d %H:%M:%S") if detail.parse_time else None,
                "parse_error": detail.parse_error
            }
        
        # 补充未找到的记录
        for file_id in file_ids:
            if file_id not in result_map:
                result_map[file_id] = {
                    "file_id": file_id,
                    "parse_status": "pending",
                    "parse_time": None,
                    "parse_error": None
                }
        
        return {
            "code": 200,
            "message": "success",
            "data": list(result_map.values()),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"批量获取解析状态失败: {str(e)}",
            "data": [],
            "timestamp": datetime.now().isoformat()
        }

# 获取节点详情 - 支持字符串 ID
@app.get("/api/v1/nodes/{node_id}")
async def get_node_detail(node_id: str):
    # 根据 ID 前缀判断节点类型
    node_type = "document"
    if node_id.startswith("theory"):
        node_type = "theory"
    elif node_id.startswith("author"):
        node_type = "author"
    elif node_id.startswith("entity"):
        node_type = "entity"
    
    # 模拟节点详情
    mock_nodes = {
        "doc_1": {
            "id": "doc_1",
            "name": "深度学习基础.pdf",
            "path": "D:/zyfdownloadanalysis/deep-learning.pdf",
            "type": "document",
            "size": 2048576,
            "extension": ".pdf",
            "bookname": "深度学习基础",
            "modified_time": "2024-02-11 14:30:25",
            "parse_status": "completed",
            "keywords": ["机器学习", "人工智能", "算法", "深度学习"],
            "abstract": "这是一份关于机器学习和人工智能的示例文档，包含了基础理论和实际应用案例。"
        },
        "theory_1": {
            "id": "theory_1",
            "name": "机器学习",
            "type": "theory",
            "doc_count": 12,
            "description": "机器学习是人工智能的一个分支，它使计算机能够从数据中学习。"
        },
        "theory_2": {
            "id": "theory_2",
            "name": "深度学习",
            "type": "theory",
            "doc_count": 8,
            "description": "深度学习是机器学习的一个子领域，使用神经网络进行学习。"
        },
        "theory_3": {
            "id": "theory_3",
            "name": "神经网络",
            "type": "theory",
            "doc_count": 6,
            "description": "神经网络是一种模拟人脑神经元连接的计算模型。"
        },
        "author_1": {
            "id": "author_1",
            "name": "张三",
            "type": "author",
            "doc_count": 4,
            "affiliation": "清华大学"
        },
        "author_2": {
            "id": "author_2",
            "name": "李四",
            "type": "author",
            "doc_count": 3,
            "affiliation": "北京大学"
        },
        "entity_1": {
            "id": "entity_1",
            "name": "Python",
            "type": "entity",
            "doc_count": 10,
            "category": "编程语言"
        },
        "entity_2": {
            "id": "entity_2",
            "name": "TensorFlow",
            "type": "entity",
            "doc_count": 7,
            "category": "深度学习框架"
        },
        "entity_3": {
            "id": "entity_3",
            "name": "监督学习",
            "type": "entity",
            "doc_count": 5,
            "category": "机器学习方法"
        }
    }
    
    # 获取节点数据，如果不存在则返回默认数据
    node_data = mock_nodes.get(node_id, {
        "id": node_id,
        "name": f"节点_{node_id}",
        "type": node_type,
        "doc_count": 1
    })
    
    return {
        "code": 200,
        "message": "success",
        "data": node_data,
        "timestamp": datetime.now().isoformat()
    }

# 搜索接口
@app.get("/api/v1/search")
async def search_nodes(q: str = ""):
    return {
        "code": 200,
        "message": "success",
        "data": {
            "query": q,
            "results": [
                {
                    "id": 3,
                    "name": "深度学习基础.pdf",
                    "type": "file",
                    "path": "D:/zyfdownloadanalysis/machine-learning/deep-learning.pdf",
                    "match_score": 0.95
                }
            ],
            "total": 1
        },
        "timestamp": datetime.now().isoformat()
    }

# 图谱统计接口
@app.get("/api/v1/graph/stats")
async def get_graph_stats():
    return {
        "code": 200,
        "message": "success",
        "data": {
            "total_documents": 1247,
            "theory_count": 156,
            "author_count": 89,
            "entity_count": 432,
            "dimension_stats": {
                "theory": {
                    "name": "理论维度",
                    "count": 156,
                    "description": "基于理论概念的知识图谱"
                },
                "author": {
                    "name": "作者维度",
                    "count": 89,
                    "description": "基于作者关系的知识图谱"
                },
                "entity": {
                    "name": "实体维度",
                    "count": 432,
                    "description": "基于实体词的知识图谱"
                }
            }
        },
        "timestamp": datetime.now().isoformat()
    }

# 图谱数据接口
@app.get("/api/v1/graph/data")
async def get_graph_data():
    # 模拟图谱节点数据 - 匹配前端 GraphData 接口
    nodes = [
        {"id": "doc_1", "type": "document", "label": "深度学习基础.pdf", "size": 25, "properties": {"abstract": "深度学习基础教程", "doc_count": 5}},
        {"id": "theory_1", "type": "theory", "label": "机器学习", "size": 40, "properties": {"doc_count": 12}},
        {"id": "theory_2", "type": "theory", "label": "深度学习", "size": 35, "properties": {"doc_count": 8}},
        {"id": "theory_3", "type": "theory", "label": "神经网络", "size": 30, "properties": {"doc_count": 6}},
        {"id": "author_1", "type": "author", "label": "张三", "size": 28, "properties": {"doc_count": 4}},
        {"id": "author_2", "type": "author", "label": "李四", "size": 25, "properties": {"doc_count": 3}},
        {"id": "entity_1", "type": "entity", "label": "Python", "size": 35, "properties": {"doc_count": 10}},
        {"id": "entity_2", "type": "entity", "label": "TensorFlow", "size": 28, "properties": {"doc_count": 7}},
        {"id": "entity_3", "type": "entity", "label": "监督学习", "size": 25, "properties": {"doc_count": 5}},
    ]
    
    # 模拟图谱边数据
    edges = [
        {"id": "e1", "source": "doc_1", "target": "theory_1", "type": "contains", "label": "涉及"},
        {"id": "e2", "source": "doc_1", "target": "theory_2", "type": "contains", "label": "涉及"},
        {"id": "e3", "source": "theory_1", "target": "theory_2", "type": "related", "label": "包含"},
        {"id": "e4", "source": "theory_2", "target": "theory_3", "type": "related", "label": "基础"},
        {"id": "e5", "source": "doc_1", "target": "author_1", "type": "authored", "label": "作者"},
        {"id": "e6", "source": "doc_1", "target": "entity_1", "type": "uses", "label": "使用"},
        {"id": "e7", "source": "entity_1", "target": "entity_2", "type": "related", "label": "库"},
        {"id": "e8", "source": "theory_1", "target": "entity_3", "type": "related", "label": "方法"},
    ]
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "dimension": "theory",
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "node_count": len(nodes),
                "edge_count": len(edges),
                "doc_count": 5
            }
        },
        "timestamp": datetime.now().isoformat()
    }

# API文档重定向
@app.get("/docs")
async def docs_redirect():
    return JSONResponse(
        content={"message": "API文档暂不可用（极简模式）", "alternative": "请查看代码中的接口定义"},
        status_code=503
    )

if __name__ == "__main__":
    print("启动极简版知识图谱系统服务器...")
    print("Python版本:", os.sys.version)
    print("服务地址: http://127.0.0.1:8000")
    print("这是极简兼容版本，避免了复杂的数据库依赖")
    print("按 Ctrl+C 停止服务器")
    print("="*50)
    
    uvicorn.run(
        "minimal_server:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=False
    )