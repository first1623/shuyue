#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档处理相关的Celery任务
"""

import logging
from celery import shared_task
from celery.exceptions import Retry
from datetime import datetime, timedelta
import time

from app.utils.document_parser import DocumentParser
from app.crawler.file_scanner import FileScanner
from app.models.data_overview import DataOverview, DataBookDetail
from app.models.user_models import ParseLog
from app.core.database import get_db, get_neo4j_session
from app.core.config import settings

logger = logging.getLogger(__name__)

@shared_task(bind=True, name="process_document", queue="document_processing")
def process_document(self, file_id: int, file_path: str = None):
    """
    处理单个文档的异步任务
    """
    task_id = self.request.id
    logger.info(f"开始处理文档任务 {task_id}, 文件ID: {file_id}")
    
    # 创建解析日志
    _create_parse_log(file_id, task_id, "processing", 0, "开始文档解析")
    
    try:
        with get_db() as db_session:
            # 获取文件信息
            file_info = db_session.query(DataOverview).filter(
                DataOverview.id == file_id,
                DataOverview.is_deleted == False
            ).first()
            
            if not file_info:
                raise ValueError(f"文件不存在或已被删除: {file_id}")
            
            if file_info.file_type != "file":
                raise ValueError(f"不是有效的文件类型: {file_info.file_type}")
            
            # 更新进度
            _update_parse_log(task_id, 10, "正在初始化解析器")
            
            # 初始化文档解析器
            parser = DocumentParser()
            
            # 更新进度
            _update_parse_log(task_id, 20, "正在解析文档内容")
            
            # 解析文档
            if not file_path:
                file_path = file_info.file_path
            
            parse_result = parser.parse_document(file_path, file_id)
            
            # 更新进度
            _update_parse_log(task_id, 80, "正在保存解析结果")
            
            # 在Neo4j中创建文档节点（如果启用了图谱）
            _create_neo4j_document_node(file_info, parse_result)
            
            # 更新进度
            _update_parse_log(task_id, 100, "文档解析完成", "completed")
            
            logger.info(f"文档处理完成 {task_id}, 文件: {file_info.file_name}")
            
            return {
                "status": "success",
                "file_id": file_id,
                "task_id": task_id,
                "parse_result": parse_result
            }
            
    except Exception as e:
        error_msg = f"文档处理失败: {str(e)}"
        logger.error(f"{error_msg}, 任务: {task_id}")
        
        # 更新解析日志
        _update_parse_log(task_id, 0, error_msg, "failed", error_msg)
        
        # 重试逻辑
        if self.request.retries < 3:
            logger.info(f"重试任务 {task_id}, 第 {self.request.retries + 1} 次")
            raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))
        
        raise

def _create_parse_log(file_id: int, task_id: str, status: str, progress: int, message: str, error_details: str = None):
    """创建解析日志"""
    try:
        with get_db() as db_session:
            log_entry = ParseLog(
                file_id=file_id,
                task_id=task_id,
                status=status,
                progress=progress,
                message=message,
                error_details=error_details,
                started_at=datetime.utcnow()
            )
            db_session.add(log_entry)
            db_session.commit()
    except Exception as e:
        logger.error(f"创建解析日志失败: {e}")

def _update_parse_log(task_id: str, progress: int, message: str, status: str = None, error_details: str = None):
    """更新解析日志"""
    try:
        with get_db() as db_session:
            log_entry = db_session.query(ParseLog).filter(
                ParseLog.task_id == task_id
            ).first()
            
            if log_entry:
                log_entry.progress = progress
                log_entry.message = message
                if status:
                    log_entry.status = status
                if error_details:
                    log_entry.error_details = error_details
                if status in ["completed", "failed"]:
                    log_entry.completed_at = datetime.utcnow()
                    # 计算耗时
                    if log_entry.started_at:
                        duration = (log_entry.completed_at - log_entry.started_at).seconds
                        log_entry.duration = duration
                
                db_session.commit()
    except Exception as e:
        logger.error(f"更新解析日志失败: {e}")

def _create_neo4j_document_node(file_info, parse_result):
    """在Neo4j中创建文档节点"""
    try:
        with get_neo4j_session() as neo4j_session:
            # 创建文档节点
            cypher = """
            MERGE (d:Document {id: $file_id})
            SET d.name = $file_name,
                d.path = $file_path,
                d.type = $file_type,
                d.extension = $extension,
                d.size = $file_size,
                d.bookname = $bookname,
                d.abstract = $abstract,
                d.keywords = $keywords,
                d.theories = $theories,
                d.parse_status = 'completed',
                d.updated_at = datetime()
            """
            
            neo4j_session.run(cypher, {
                'file_id': file_info.id,
                'file_name': file_info.file_name,
                'file_path': file_info.file_path,
                'file_type': file_info.file_type,
                'extension': file_info.file_extension,
                'file_size': file_info.file_size,
                'bookname': file_info.bookname,
                'abstract': parse_result.get('abstract', ''),
                'keywords': parse_result.get('keywords', []),
                'theories': parse_result.get('theories', [])
            })
            
            # 如果有父文件夹，创建包含关系
            if file_info.parent_id:
                parent_cypher = """
                MATCH (f:Folder {id: $parent_id}), (d:Document {id: $file_id})
                MERGE (f)-[:CONTAINS]->(d)
                """
                neo4j_session.run(parent_cypher, {
                    'parent_id': file_info.parent_id,
                    'file_id': file_info.id
                })
                
    except Exception as e:
        logger.warning(f"Neo4j节点创建失败: {e}")
        # Neo4j连接失败不应影响主要业务流程

@shared_task(bind=True, name="batch_process_documents", queue="document_processing")
def batch_process_documents(self, file_ids: list = None, limit: int = 10):
    """
    批量处理文档的异步任务
    """
    task_id = self.request.id
    logger.info(f"开始批量处理文档任务 {task_id}, 文件数量: {len(file_ids) if file_ids else limit}")
    
    try:
        with get_db() as db_session:
            # 查询待解析的文档
            query = db_session.query(DataOverview).filter(
                DataOverview.file_type == "file",
                DataOverview.is_deleted == False
            )
            
            # 过滤出支持的文档类型且未解析的
            supported_extensions = settings.SUPPORTED_EXTENSIONS
            query = query.filter(DataOverview.file_extension.in_(supported_extensions))
            
            # 排除已解析的文档
            subquery = db_session.query(DataBookDetail.file_id).filter(
                DataBookDetail.parse_status == "completed"
            ).subquery()
            query = query.filter(~DataOverview.id.in_(subquery))
            
            # 应用限制
            if file_ids:
                query = query.filter(DataOverview.id.in_(file_ids))
            else:
                query = query.limit(limit)
            
            files_to_process = query.all()
            
            if not files_to_process:
                logger.info("没有找到需要处理的文档")
                return {"status": "completed", "processed": 0, "message": "没有需要处理的文档"}
            
            processed_count = 0
            failed_count = 0
            
            # 逐个处理文档
            for file_info in files_to_process:
                try:
                    # 为每个文件创建独立的任务
                    process_document.delay(file_info.id)
                    processed_count += 1
                    
                    # 避免并发过多，添加小延迟
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"排队处理文件失败 {file_info.id}: {e}")
                    failed_count += 1
            
            result = {
                "status": "completed",
                "task_id": task_id,
                "total_files": len(files_to_process),
                "processed": processed_count,
                "failed": failed_count,
                "message": f"批量处理任务已完成，成功排队 {processed_count} 个文件"
            }
            
            logger.info(f"批量处理任务完成 {task_id}: {result}")
            return result
            
    except Exception as e:
        error_msg = f"批量处理任务失败: {str(e)}"
        logger.error(f"{error_msg}, 任务: {task_id}")
        raise

@shared_task(bind=True, name="scan_filesystem", queue="document_processing")
def scan_filesystem_task(self):
    """
    文件系统扫描的异步任务
    """
    task_id = self.request.id
    logger.info(f"开始文件系统扫描任务 {task_id}")
    
    try:
        scanner = FileScanner()
        
        with get_db() as db_session:
            result = scanner.scan_filesystem(db_session)
            
            # 获取扫描统计信息
            stats = scanner.get_scan_statistics(db_session)
            
            logger.info(f"文件系统扫描完成 {task_id}: {stats}")
            
            return {
                "status": "success",
                "task_id": task_id,
                "scan_result": result,
                "statistics": stats
            }
            
    except Exception as e:
        error_msg = f"文件系统扫描失败: {str(e)}"
        logger.error(f"{error_msg}, 任务: {task_id}")
        raise self.retry(exc=e, countdown=300)  # 5分钟后重试