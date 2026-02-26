#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识树相关API视图
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.core.database import get_db
from app.models.data_overview import DataOverview, DataBookDetail
from app.crawler.file_scanner import FileScanner
from app.tasks.document_tasks import scan_filesystem_task, batch_process_documents
from app.schemas.knowledge_tree import KnowledgeTreeResponse, TreeNode

router = APIRouter(prefix="/knowledge-tree", tags=["knowledge_tree"])

@router.get("/tree", response_model=KnowledgeTreeResponse)
async def get_knowledge_tree(
    db: Session = Depends(get_db),
    include_files: bool = Query(True, description="是否包含文件节点"),
    max_depth: Optional[int] = Query(None, description="最大深度限制"),
    file_types: Optional[List[str]] = Query(None, description="文件类型过滤")
):
    """
    获取完整的知识树结构
    """
    try:
        # 构建查询条件
        query = db.query(DataOverview).filter(DataOverview.is_deleted == False)
        
        if not include_files:
            query = query.filter(DataOverview.file_type == "folder")
        
        if file_types:
            query = query.filter(DataOverview.file_extension.in_(file_types))
        
        # 获取所有节点并按路径排序
        nodes = query.order_by(DataOverview.file_path).all()
        
        # 构建树形结构
        tree_nodes = _build_tree_structure(nodes, max_depth)
        
        # 获取统计信息
        stats = {
            "total_nodes": len(nodes),
            "folders": len([n for n in nodes if n.file_type == "folder"]),
            "files": len([n for n in nodes if n.file_type == "file"]),
            "supported_docs": len([n for n in nodes if n.file_extension in [".pdf", ".docx", ".txt", ".md"]])
        }
        
        return KnowledgeTreeResponse(
            status="success",
            tree=tree_nodes,
            statistics=stats
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取知识树失败: {str(e)}")

@router.post("/scan")
async def trigger_file_scan(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    触发文件系统扫描
    """
    try:
        # 在后台执行扫描任务
        task = scan_filesystem_task.delay()
        
        return JSONResponse({
            "status": "success",
            "message": "文件系统扫描已开始",
            "task_id": task.id
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动扫描任务失败: {str(e)}")

@router.get("/node/{node_id}")
async def get_node_details(
    node_id: int,
    db: Session = Depends(get_db)
):
    """
    获取特定节点的详细信息
    """
    try:
        node = db.query(DataOverview).filter(
            DataOverview.id == node_id,
            DataOverview.is_deleted == False
        ).first()
        
        if not node:
            raise HTTPException(status_code=404, detail="节点不存在")
        
        # 获取子节点
        children = db.query(DataOverview).filter(
            DataOverview.parent_id == node_id,
            DataOverview.is_deleted == False
        ).order_by(DataOverview.file_name).all()
        
        # 构建节点信息
        node_info = {
            "id": node.id,
            "name": node.file_name,
            "path": node.file_path,
            "type": node.file_type,
            "size": node.file_size,
            "extension": node.file_extension,
            "bookname": node.bookname,
            "modified_time": node.modified_time.isoformat() if node.modified_time else None,
            "children": [
                {
                    "id": child.id,
                    "name": child.file_name,
                    "type": child.file_type,
                    "extension": child.file_extension,
                    "size": child.file_size
                }
                for child in children
            ]
        }
        
        return JSONResponse({
            "status": "success",
            "node": node_info
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取节点详情失败: {str(e)}")

@router.post("/process-documents")
async def trigger_document_processing(
    background_tasks: BackgroundTasks,
    file_ids: Optional[List[int]] = None,
    limit: int = Query(10, ge=1, le=100, description="处理文件数量限制")
):
    """
    触发文档批量处理
    """
    try:
        # 启动批量处理任务
        task = batch_process_documents.delay(file_ids, limit)
        
        return JSONResponse({
            "status": "success",
            "message": "文档处理任务已开始",
            "task_id": task.id,
            "file_ids": file_ids,
            "limit": limit
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动文档处理任务失败: {str(e)}")

@router.get("/statistics")
async def get_tree_statistics(
    db: Session = Depends(get_db)
):
    """
    获取知识树统计信息
    """
    try:
        from sqlalchemy import func
        
        # 基础统计
        total_files = db.query(DataOverview).filter(
            DataOverview.file_type == "file",
            DataOverview.is_deleted == False
        ).count()
        
        total_folders = db.query(DataOverview).filter(
            DataOverview.file_type == "folder",
            DataOverview.is_deleted == False
        ).count()
        
        # 按文件类型统计
        file_type_stats = db.query(
            DataOverview.file_extension,
            func.count(DataOverview.id)
        ).filter(
            DataOverview.file_type == "file",
            DataOverview.is_deleted == False,
            DataOverview.file_extension.isnot(None)
        ).group_by(DataOverview.file_extension).all()
        
        # 解析状态统计
        parse_stats = db.query(
            DataOverview.file_extension,
            func.count(DataBookDetail.id).label('parsed_count')
        ).outerjoin(
            DataBookDetail,
            DataOverview.id == DataBookDetail.file_id
        ).filter(
            DataOverview.file_type == "file",
            DataOverview.is_deleted == False,
            DataOverview.file_extension.in_([".pdf", ".docx", ".txt", ".md"])
        ).group_by(DataOverview.file_extension).all()
        
        # 总文件大小
        total_size = db.query(func.sum(DataOverview.file_size)).filter(
            DataOverview.file_type == "file",
            DataOverview.is_deleted == False
        ).scalar() or 0
        
        return JSONResponse({
            "status": "success",
            "statistics": {
                "total_files": total_files,
                "total_folders": total_folders,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024*1024), 2),
                "file_types": {
                    ext: count for ext, count in file_type_stats
                },
                "parse_status": {
                    ext: parsed_count for ext, parsed_count in parse_stats
                }
            }
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")

def _build_tree_structure(nodes: List[DataOverview], max_depth: Optional[int] = None) -> List[dict]:
    """
    构建树形结构
    """
    # 创建节点映射
    node_map = {node.id: {
        "id": node.id,
        "name": node.file_name,
        "path": node.file_path,
        "type": node.file_type,
        "size": node.file_size,
        "extension": node.file_extension,
        "bookname": node.bookname,
        "modified_time": node.modified_time.isoformat() if node.modified_time else None,
        "children": []
    } for node in nodes}
    
    # 构建父子关系
    root_nodes = []
    
    for node in nodes:
        if node.parent_id is None:
            root_nodes.append(node_map[node.id])
        elif node.parent_id in node_map:
            parent = node_map[node.parent_id]
            if max_depth is None or _get_node_depth(node_map, node.id) <= max_depth:
                parent["children"].append(node_map[node.id])
    
    # 排序子节点
    def sort_children(node):
        if node["children"]:
            node["children"].sort(key=lambda x: (x["type"] == "file", x["name"].lower()))
            for child in node["children"]:
                sort_children(child)
    
    for root in root_nodes:
        sort_children(root)
    
    return sorted(root_nodes, key=lambda x: x["name"].lower())

def _get_node_depth(node_map: dict, node_id: int, current_depth: int = 0) -> int:
    """
    计算节点深度
    """
    node = next((n for n in node_map.values() if n["id"] == node_id), None)
    if not node or "_visited" in node:
        return current_depth
    
    node["_visited"] = True
    
    # 查找父节点
    parent_node = None
    for n in node_map.values():
        if node_id in [child["id"] for child in n.get("children", [])]:
            parent_node = n
            break
    
    if parent_node:
        return _get_node_depth(node_map, parent_node["id"], current_depth + 1)
    
    return current_depth


@router.get("/scanned-files")
async def get_scanned_files(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=500, description="返回的记录数")
):
    """
    获取已扫描的文件列表
    """
    try:
        # 获取所有文件
        files_query = db.query(DataOverview).filter(
            DataOverview.file_type == "file",
            DataOverview.is_deleted == False
        ).order_by(DataOverview.modified_time.desc())
        
        files = files_query.offset(skip).limit(limit).all()
        total_files = files_query.count()
        
        # 获取所有文件夹
        folders = db.query(DataOverview).filter(
            DataOverview.file_type == "folder",
            DataOverview.is_deleted == False
        ).all()
        
        # 格式化文件列表
        file_list = []
        for file in files:
            # 获取解析状态
            detail = db.query(DataBookDetail).filter(
                DataBookDetail.file_id == file.id
            ).first()
            
            file_list.append({
                "id": file.id,
                "name": file.file_name,
                "path": file.file_path,
                "extension": file.file_extension,
                "size": file.file_size,
                "modified_time": file.modified_time.isoformat() if file.modified_time else None,
                "parse_status": "completed" if detail else "pending",
                "bookname": file.bookname
            })
        
        # 格式化文件夹列表
        folder_list = [{
            "id": folder.id,
            "name": folder.file_name,
            "path": folder.file_path
        } for folder in folders[:50]]  # 限制返回50个文件夹
        
        return JSONResponse({
            "code": 200,
            "message": "success",
            "data": {
                "files": file_list,
                "folders": folder_list,
                "total_files": total_files,
                "total_folders": len(folders)
            }
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取已扫描文件失败: {str(e)}")


@router.get("/files/{file_id}/preview")
async def preview_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    """
    预览文件内容
    """
    try:
        # 获取文件信息
        file = db.query(DataOverview).filter(
            DataOverview.id == file_id,
            DataOverview.is_deleted == False
        ).first()
        
        if not file:
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 获取解析详情
        detail = db.query(DataBookDetail).filter(
            DataBookDetail.file_id == file_id
        ).first()
        
        content = ""
        
        # 如果已解析，返回解析内容
        if detail:
            content = detail.content or detail.abstract or "暂无解析内容"
        else:
            # 尝试直接读取文件内容（仅限文本文件）
            try:
                import os
                if file.file_path and os.path.exists(file.file_path):
                    # 限制只读取文本类型文件
                    text_extensions = ['.txt', '.md', '.json', '.csv', '.xml', '.html', '.css', '.js', '.py']
                    if file.file_extension and file.file_extension.lower() in text_extensions:
                        with open(file.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            # 只读取前10000个字符
                            content = f.read(10000)
                    else:
                        content = f"文件类型 {file.file_extension} 暂不支持预览，请先解析文档"
                else:
                    content = "文件路径不存在或无法访问"
            except Exception as e:
                content = f"读取文件失败: {str(e)}"
        
        return JSONResponse({
            "code": 200,
            "message": "success",
            "data": {
                "id": file.id,
                "name": file.file_name,
                "path": file.file_path,
                "extension": file.file_extension,
                "size": file.file_size,
                "parse_status": "completed" if detail else "pending",
                "content": content
            }
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"预览文件失败: {str(e)}")