#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Celery异步任务配置
"""

import os
from celery import Celery
from kombu import Queue
from app.core.config import settings

# 创建Celery实例
celery_app = Celery(
    "knowledge_graph_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.document_tasks",
        "app.tasks.graph_tasks",
        "app.tasks.maintenance_tasks"
    ]
)

# Celery配置
celery_app.conf.update(
    # 任务序列化
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    
    # 任务路由
    task_routes={
        "app.tasks.document_tasks.*": {"queue": "document_processing"},
        "app.tasks.graph_tasks.*": {"queue": "graph_operations"},
        "app.tasks.maintenance_tasks.*": {"queue": "maintenance"},
    },
    
    # 任务队列
    task_default_queue="default",
    task_queues=(
        Queue("default", routing_key="task.default"),
        Queue("document_processing", routing_key="task.document"),
        Queue("graph_operations", routing_key="task.graph"),
        Queue("maintenance", routing_key="task.maintenance"),
    ),
    
    # 任务执行设置
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_reject_on_worker_lost=True,
    
    # 结果过期时间
    result_expires=3600,  # 1小时
    
    # 任务软时间限制
    task_soft_time_limit=1800,  # 30分钟
    task_time_limit=3600,  # 1小时
    
    # 错误处理
    task_annotations={
        "*": {
            "rate_limit": "10/m",  # 每分钟最多10个任务
            "max_retries": 3,
        }
    },
    
    # 监控
    worker_send_task_events=True,
    task_send_sent_event=True,
)

# 导入任务模块（确保任务被注册）
from app.tasks import document_tasks, graph_tasks, maintenance_tasks