#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data_overview 表模型 - 文件和文件夹信息
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel

class DataOverview(BaseModel):
    """文件和文件夹信息表"""
    __tablename__ = "data_overview"
    
    # 基本信息
    file_name = Column(String(255), nullable=False, comment="文件名")
    file_path = Column(Text, nullable=False, unique=True, comment="完整路径")
    file_type = Column(String(50), nullable=False, comment="文件类型：folder/file")
    parent_id = Column(Integer, ForeignKey("data_overview.id", ondelete="CASCADE"), nullable=True, comment="父节点ID")
    
    # 扩展信息
    file_size = Column(Integer, nullable=True, comment="文件大小（字节）")
    download_time = Column(DateTime, nullable=True, comment="下载时间")
    bookname = Column(String(500), nullable=True, comment="书籍文档名称")
    file_extension = Column(String(10), nullable=True, comment="文件扩展名")
    modified_time = Column(DateTime, nullable=True, comment="文件修改时间")
    is_deleted = Column(Boolean, default=False, comment="是否删除")
    doc_metadata = Column(JSON, nullable=True, comment="额外元数据")
    
    # 索引
    __table_args__ = (
        {"comment": "文件和文件夹信息表"},
    )
    
    # 关系
    children = relationship("DataOverview", backref="parent", remote_side="DataOverview.id")
    book_detail = relationship("DataBookDetail", back_populates="file_info", uselist=False)
    # TODO: 后续添加文档关系图谱时启用
    # relationships_as_source = relationship("DataRelationship", foreign_keys="DataRelationship.source_id", back_populates="source_node")
    # relationships_as_target = relationship("DataRelationship", foreign_keys="DataRelationship.target_id", back_populates="target_node")

class DataBookDetail(BaseModel):
    """文档详细信息表"""
    __tablename__ = "data_book_detail"
    
    # 关联信息
    file_id = Column(Integer, ForeignKey("data_overview.id", ondelete="CASCADE"), nullable=False, comment="关联data_overview表")
    
    # 解析内容
    abstract = Column(Text, nullable=True, comment="摘要信息")
    keywords = Column(JSON, nullable=True, comment="关键词列表")
    theories = Column(JSON, nullable=True, comment="引用的理论/参考文献")
    experiment_flow = Column(Text, nullable=True, comment="实验流程概述")
    statistical_methods = Column(JSON, nullable=True, comment="使用的统计方法")
    conclusion = Column(Text, nullable=True, comment="研究结论")
    full_text = Column(Text, nullable=True, comment="全文存储（可选）")
    
    # 三维度图谱字段（新增）
    authors = Column(JSON, nullable=True, comment="文档作者列表（支持多作者）")
    theories_used = Column(JSON, nullable=True, comment="使用的理论/依据（来自DeepSeek解析）")
    entities = Column(JSON, nullable=True, comment="提取的实体词（人名、地名、术语等）")
    entity_relations = Column(JSON, nullable=True, comment="实体间关系（如共现、引用）")
    
    # 解析状态
    parse_status = Column(String(20), default="pending", comment="解析状态：pending/processing/completed/failed")
    parse_time = Column(DateTime, nullable=True, comment="解析时间")
    parse_error = Column(Text, nullable=True, comment="解析错误信息")
    deepseek_response = Column(JSON, nullable=True, comment="DeepSeek API原始响应")
    
    # 索引
    __table_args__ = (
        {"comment": "文档详细信息表"},
    )
    
    # 关系
    file_info = relationship("DataOverview", back_populates="book_detail")