#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习平台知识图谱与文档解析系统 - 主应用入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.core.config import settings
from app.core.database import init_db
from app.views import knowledge_tree, node_detail, graph_visualization, search, user

# 创建FastAPI应用实例
app = FastAPI(
    title="学习平台知识图谱系统",
    description="基于文件夹结构自动构建知识图谱，支持文档智能解析、关系提取和可视化展示",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(knowledge_tree.router, prefix="/api/v1", tags=["knowledge_tree"])
app.include_router(node_detail.router, prefix="/api/v1", tags=["node_detail"])
app.include_router(graph_visualization.router, prefix="/api/v1", tags=["graph"])
app.include_router(search.router, prefix="/api/v1", tags=["search"])
app.include_router(user.router, prefix="/api/v1", tags=["user"])

# 静态文件服务（用于上传的文件）
app.mount("/uploads", StaticFiles(directory="data/uploads"), name="uploads")

@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化操作"""
    await init_db()
    print("应用启动完成，数据库连接已初始化")

@app.get("/")
async def root():
    """根路径健康检查"""
    return {
        "message": "学习平台知识图谱系统API服务",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "service": "knowledge_graph_api"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )