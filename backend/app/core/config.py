#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用配置文件
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 应用基础配置
    PROJECT_NAME: str = "学习平台知识图谱系统"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 数据库配置 - 默认使用 SQLite，方便部署
    # 可通过环境变量 DATABASE_URL 切换到 PostgreSQL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/knowledge_graph.db")
    
    # PostgreSQL 配置（备用）
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "username"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "knowledge_graph"
    
    # Neo4j图数据库配置
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"

    # Redis配置
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0

    # Celery配置
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # DeepSeek API配置
    DEEPSEEK_API_KEY: str = "your-deepseek-api-key"
    DEEPSEEK_API_BASE: str = "https://api.deepseek.com"
    DEEPSEEK_MODEL: str = "deepseek-chat"
    
    # DeepSeek 缓存配置
    DEEPSEEK_CACHE_ENABLED: bool = True
    DEEPSEEK_CACHE_DIR: str = "data/deepseek_cache"
    DEEPSEEK_CACHE_MAX_SIZE_MB: int = 500
    DEEPSEEK_CACHE_TTL_HOURS: int = 168  # 7天
    
    # DeepSeek 重试配置
    DEEPSEEK_RETRY_MAX_RETRIES: int = 3
    DEEPSEEK_RETRY_BASE_DELAY: float = 1.0
    DEEPSEEK_RETRY_MAX_DELAY: float = 60.0
    DEEPSEEK_RETRY_EXPONENTIAL_BASE: float = 2.0
    DEEPSEEK_RETRY_JITTER: bool = True
    DEEPSEEK_CIRCUIT_BREAKER_ENABLED: bool = True
    DEEPSEEK_CIRCUIT_FAILURE_THRESHOLD: int = 5
    DEEPSEEK_CIRCUIT_RECOVERY_TIMEOUT: int = 60
    DEEPSEEK_REQUEST_TIMEOUT: int = 60
    
    # 文件扫描配置
    SCAN_PATH: str = r"D:\zyfdownloadanalysis"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    
    # 支持的文档格式
    SUPPORTED_EXTENSIONS: List[str] = [".pdf", ".docx", ".txt", ".md"]
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ]
    
    # 文件上传配置
    UPLOAD_DIR: str = "data/uploads"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"  # 允许 .env 中有额外字段
        
settings = Settings()