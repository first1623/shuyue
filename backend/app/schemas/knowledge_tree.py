#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识树相关的Pydantic模型
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class TreeNode(BaseModel):
    """树节点模型"""
    id: int
    name: str
    path: str
    type: str  # "folder" or "file"
    size: Optional[int] = None
    extension: Optional[str] = None
    bookname: Optional[str] = None
    modified_time: Optional[str] = None
    children: Optional[List['TreeNode']] = None
    
    class Config:
        from_attributes = True

class KnowledgeTreeResponse(BaseModel):
    """知识树响应模型"""
    status: str
    tree: List[TreeNode]
    statistics: Dict[str, Any]
    
    class Config:
        from_attributes = True

class ScanRequest(BaseModel):
    """扫描请求模型"""
    scan_path: Optional[str] = None
    include_hidden: bool = False
    max_depth: Optional[int] = None

class ProcessDocumentsRequest(BaseModel):
    """文档处理请求模型"""
    file_ids: Optional[List[int]] = None
    limit: int = 10
    priority_extensions: Optional[List[str]] = None

class StatisticsResponse(BaseModel):
    """统计信息响应模型"""
    status: str
    statistics: Dict[str, Any]
    
    class Config:
        from_attributes = True

# 更新前向引用
TreeNode.model_rebuild()