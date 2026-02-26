#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data_relationship 表模型 - 关系数据
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from datetime import datetime
from app.models.base import BaseModel

class RelationType(PyEnum):
    """关系类型枚举"""
    CONTAINS = "contains"           # 包含关系（文件夹-文件）
    REFERENCES = "references"       # 引用关系（文档A引用文档B）
    SIMILAR_TOPIC = "similar_topic" # 相似主题关系
    SHARED_THEORY = "shared_theory" # 共用理论关系
    AUTHOR = "author"               # 作者关系
    INSTITUTION = "institution"     # 机构关系

class DataRelationship(BaseModel):
    """数据关系表"""
    __tablename__ = "data_relationship"
    
    # 关系节点
    source_id = Column(Integer, ForeignKey("data_overview.id", ondelete="CASCADE"), nullable=False, comment="源节点ID")
    target_id = Column(Integer, ForeignKey("data_overview.id", ondelete="CASCADE"), nullable=False, comment="目标节点ID")
    
    # 关系信息
    relation_type = Column(Enum(RelationType), nullable=False, comment="关系类型")
    weight = Column(Float, default=1.0, comment="关联强度（0-1）")
    description = Column(Text, nullable=True, comment="关系描述")
    confidence = Column(Float, default=1.0, comment="关系置信度（0-1）")
    
    # 元数据
    evidence = Column(Text, nullable=True, comment="关系证据说明")
    auto_generated = Column(Boolean, default=True, comment="是否自动生成")
    validated = Column(Boolean, default=False, comment="是否已验证")
    
    # 索引
    __table_args__ = (
        {"comment": "数据关系表"},
    )
    
    # 关系
    source_node = relationship("DataOverview", foreign_keys=[source_id], back_populates="relationships_as_source")
    target_node = relationship("DataOverview", foreign_keys=[target_id], back_populates="relationships_as_target")