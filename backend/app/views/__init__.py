#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视图模块初始化文件
"""

# 只导入存在的模块
from app.views import knowledge_tree

# 为了向后兼容，创建占位符模块
class PlaceholderRouter:
    def __init__(self):
        from fastapi import APIRouter
        self.router = APIRouter()
        
        @self.router.get("/placeholder")
        def placeholder():
            return {"message": "该功能模块正在开发中"}

# 为缺失的模块创建占位符
node_detail = PlaceholderRouter()
graph_visualization = PlaceholderRouter()
search = PlaceholderRouter()
user = PlaceholderRouter()

__all__ = [
    'knowledge_tree',
    'node_detail', 
    'graph_visualization',
    'search',
    'user'
]