#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户相关模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel

class User(BaseModel):
    """用户表"""
    __tablename__ = "user"
    
    username = Column(String(50), unique=True, nullable=False, comment="用户名")
    email = Column(String(100), unique=True, nullable=False, comment="邮箱")
    hashed_password = Column(String(255), nullable=False, comment="加密密码")
    full_name = Column(String(100), nullable=True, comment="全名")
    avatar_url = Column(String(255), nullable=True, comment="头像URL")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_superuser = Column(Boolean, default=False, comment="是否超级用户")
    last_login = Column(DateTime, nullable=True, comment="最后登录时间")
    preferences = Column(JSON, nullable=True, comment="用户偏好设置")
    
    # 关系
    favorites = relationship("UserFavorite", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("NodeComment", back_populates="user", cascade="all, delete-orphan")
    search_history = relationship("SearchHistory", back_populates="user", cascade="all, delete-orphan")
    
    __table_args__ = (
        {"comment": "用户信息表"},
    )

class UserFavorite(BaseModel):
    """用户收藏表"""
    __tablename__ = "user_favorite"
    
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    node_id = Column(Integer, ForeignKey("data_overview.id", ondelete="CASCADE"), nullable=False, comment="节点ID")
    favorite_type = Column(String(20), default="node", comment="收藏类型")
    notes = Column(Text, nullable=True, comment="收藏备注")
    
    # 关系
    user = relationship("User", back_populates="favorites")
    node = relationship("DataOverview")
    
    __table_args__ = (
        {"comment": "用户收藏节点表"},
    )

class Tag(BaseModel):
    """标签表"""
    __tablename__ = "tag"
    
    name = Column(String(50), unique=True, nullable=False, comment="标签名称")
    color = Column(String(7), default="#1890ff", comment="标签颜色")
    description = Column(String(200), nullable=True, comment="标签描述")
    category = Column(String(50), nullable=True, comment="标签分类")
    usage_count = Column(Integer, default=0, comment="使用次数")
    
    # 关系
    file_tags = relationship("FileTag", back_populates="tag", cascade="all, delete-orphan")
    
    __table_args__ = (
        {"comment": "标签表"},
    )

class FileTag(BaseModel):
    """文件标签关联表"""
    __tablename__ = "file_tag"
    
    file_id = Column(Integer, ForeignKey("data_overview.id", ondelete="CASCADE"), nullable=False, comment="文件ID")
    tag_id = Column(Integer, ForeignKey("tag.id", ondelete="CASCADE"), nullable=False, comment="标签ID")
    
    # 关系
    file = relationship("DataOverview")
    tag = relationship("Tag", back_populates="file_tags")
    
    __table_args__ = (
        {"comment": "文件标签关联表"},
    )

class NodeComment(BaseModel):
    """节点批注/笔记表"""
    __tablename__ = "node_comment"
    
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    node_id = Column(Integer, ForeignKey("data_overview.id", ondelete="CASCADE"), nullable=False, comment="节点ID")
    content = Column(Text, nullable=False, comment="批注内容")
    comment_type = Column(String(20), default="note", comment="批注类型")
    position = Column(JSON, nullable=True, comment="批注位置信息")
    is_public = Column(Boolean, default=False, comment="是否公开")
    
    # 关系
    user = relationship("User", back_populates="comments")
    node = relationship("DataOverview")
    
    __table_args__ = (
        {"comment": "节点批注笔记表"},
    )

class ParseLog(BaseModel):
    """解析任务日志表"""
    __tablename__ = "parse_log"
    
    file_id = Column(Integer, ForeignKey("data_overview.id", ondelete="SET NULL"), nullable=True, comment="文件ID")
    task_id = Column(String(100), nullable=False, comment="任务ID")
    status = Column(String(20), nullable=False, comment="任务状态")
    progress = Column(Integer, default=0, comment="进度百分比")
    message = Column(Text, nullable=True, comment="状态消息")
    error_details = Column(Text, nullable=True, comment="错误详情")
    started_at = Column(DateTime, nullable=False, comment="开始时间")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")
    duration = Column(Integer, nullable=True, comment="耗时（秒）")
    
    __table_args__ = (
        {"comment": "解析任务日志表"},
    )

class SearchHistory(BaseModel):
    """用户搜索记录表"""
    __tablename__ = "search_history"
    
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    query = Column(String(500), nullable=False, comment="搜索查询")
    search_type = Column(String(50), nullable=True, comment="搜索类型")
    filters = Column(JSON, nullable=True, comment="搜索过滤器")
    results_count = Column(Integer, default=0, comment="结果数量")
    
    # 关系
    user = relationship("User", back_populates="search_history")
    
    __table_args__ = (
        {"comment": "用户搜索记录表"},
    )