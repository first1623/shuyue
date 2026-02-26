#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件系统扫描器 - 递归扫描文件夹结构并构建知识树
"""

import os
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import magic
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.core.config import settings
from app.models.data_overview import DataOverview
from app.core.database import get_db

class FileScanner:
    """文件系统扫描器"""
    
    def __init__(self):
        self.scan_path = Path(settings.SCAN_PATH)
        self.supported_extensions = settings.SUPPORTED_EXTENSIONS
        self.max_file_size = settings.MAX_FILE_SIZE
        self.executor = ThreadPoolExecutor(max_workers=4)
        
    def scan_filesystem(self, db_session) -> Dict:
        """扫描文件系统并构建知识树"""
        print(f"开始扫描文件系统: {self.scan_path}")
        
        if not self.scan_path.exists():
            raise FileNotFoundError(f"扫描路径不存在: {self.scan_path}")
        
        # 清空现有数据（可选，根据需求调整）
        # self._clear_existing_data(db_session)
        
        # 构建文件树
        file_tree = self._build_file_tree(db_session)
        
        print(f"扫描完成，共发现 {len(file_tree)} 个节点")
        return {
            "status": "success",
            "scanned_path": str(self.scan_path),
            "total_nodes": len(file_tree),
            "tree": file_tree
        }
    
    def _build_file_tree(self, db_session) -> List[Dict]:
        """构建文件树结构"""
        nodes = []
        node_id_map = {}  # 路径到ID的映射
        
        def traverse_directory(current_path: Path, parent_id: Optional[int] = None, depth: int = 0) -> int:
            """递归遍历目录"""
            if depth > 20:  # 防止无限递归
                return None
                
            # 跳过隐藏文件和系统文件
            if current_path.name.startswith('.') or current_path.name.startswith('~$'):
                return None
            
            # 生成唯一ID（使用路径的hash）
            path_hash = hashlib.md5(str(current_path).encode()).hexdigest()[:8]
            unique_id = f"{depth}_{path_hash}"
            
            # 判断是文件还是文件夹
            is_file = current_path.is_file()
            file_type = "file" if is_file else "folder"
            
            # 获取文件信息
            file_stat = current_path.stat()
            file_size = file_stat.st_size if is_file else None
            modified_time = datetime.fromtimestamp(file_stat.st_mtime)
            
            # 获取文件扩展名
            file_extension = current_path.suffix.lower() if is_file else None
            
            # 检查是否为支持的文档类型
            is_supported_doc = is_file and file_extension in self.supported_extensions
            
            # 提取书名（如果是文档文件）
            bookname = None
            if is_supported_doc:
                bookname = self._extract_book_name(current_path)
            
            # 创建数据库记录
            file_info = DataOverview(
                file_name=current_path.name,
                file_path=str(current_path),
                file_type=file_type,
                parent_id=parent_id,
                file_size=file_size,
                modified_time=modified_time,
                file_extension=file_extension,
                bookname=bookname,
                is_deleted=False
            )
            
            db_session.add(file_info)
            db_session.flush()  # 获取ID但不提交
            
            # 构建节点信息
            node_info = {
                "id": file_info.id,
                "unique_id": unique_id,
                "name": current_path.name,
                "path": str(current_path),
                "type": file_type,
                "size": file_size,
                "extension": file_extension,
                "modified_time": modified_time.isoformat(),
                "bookname": bookname,
                "is_supported_doc": is_supported_doc,
                "children": [] if not is_file else None,
                "depth": depth
            }
            
            node_id_map[str(current_path)] = file_info.id
            nodes.append(node_info)
            
            # 如果是文件夹，递归处理子项
            if not is_file:
                try:
                    children = []
                    for child_path in current_path.iterdir():
                        child_id = traverse_directory(child_path, file_info.id, depth + 1)
                        if child_id:
                            children.append(child_id)
                    
                    if children:
                        # 按名称和类型排序
                        children.sort(key=lambda x: (nodes[x-1]["type"] == "file", nodes[x-1]["name"]))
                        node_info["children"] = children
                        
                except PermissionError:
                    print(f"权限不足，跳过目录: {current_path}")
                except OSError as e:
                    print(f"访问目录出错 {current_path}: {e}")
            
            return file_info.id
        
        # 开始遍历
        traverse_directory(self.scan_path)
        
        # 提交数据库事务
        db_session.commit()
        
        return nodes
    
    def _extract_book_name(self, file_path: Path) -> Optional[str]:
        """从文件路径提取书名"""
        name = file_path.stem  # 不含扩展名的文件名
        
        # 清理常见的文件名模式
        import re
        
        # 移除版本号、日期等
        name = re.sub(r'[\d]{4}[\d\-_\.]*', '', name)  # 移除年份和日期
        name = re.sub(r'[vV]\d+\.\d+', '', name)  # 移除版本号
        name = re.sub(r'[_\-\.]\d+$', '', name)  # 移除末尾数字
        
        # 替换分隔符为空格
        name = re.sub(r'[._\-]+', ' ', name)
        
        # 首字母大写
        name = name.strip().title()
        
        return name if len(name) > 2 else None
    
    def _get_file_mime_type(self, file_path: Path) -> str:
        """获取文件MIME类型"""
        try:
            mime = magic.from_file(str(file_path), mime=True)
            return mime
        except:
            return "application/octet-stream"
    
    def _clear_existing_data(self, db_session):
        """清空现有数据（谨慎使用）"""
        print("清空现有文件数据...")
        db_session.query(DataOverview).delete()
        db_session.commit()
    
    async def scan_async(self) -> Dict:
        """异步扫描文件系统"""
        loop = asyncio.get_event_loop()
        
        with get_db() as db_session:
            result = await loop.run_in_executor(
                self.executor, 
                self.scan_filesystem, 
                db_session
            )
            return result
    
    def get_scan_statistics(self, db_session) -> Dict:
        """获取扫描统计信息"""
        from sqlalchemy import func
        
        total_files = db_session.query(DataOverview).filter(
            DataOverview.file_type == "file",
            DataOverview.is_deleted == False
        ).count()
        
        total_folders = db_session.query(DataOverview).filter(
            DataOverview.file_type == "folder",
            DataOverview.is_deleted == False
        ).count()
        
        supported_docs = db_session.query(DataOverview).filter(
            DataOverview.file_type == "file",
            DataOverview.file_extension.in_(self.supported_extensions),
            DataOverview.is_deleted == False
        ).count()
        
        total_size = db_session.query(func.sum(DataOverview.file_size)).filter(
            DataOverview.file_type == "file",
            DataOverview.is_deleted == False
        ).scalar() or 0
        
        return {
            "total_files": total_files,
            "total_folders": total_folders,
            "supported_documents": supported_docs,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024*1024), 2)
        }