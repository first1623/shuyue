#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek API 响应缓存模块
支持基于内容哈希的本地缓存和可选的 Redis 缓存
"""

import os
import json
import hashlib
import logging
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
import threading
import pickle

logger = logging.getLogger(__name__)


class DeepSeekCache:
    """DeepSeek API 响应缓存管理器"""
    
    def __init__(
        self,
        cache_dir: str = None,
        max_cache_size_mb: int = 500,
        cache_ttl_hours: int = 168,  # 默认7天
        enable_cache: bool = True
    ):
        """
        初始化缓存管理器
        
        Args:
            cache_dir: 缓存目录路径
            max_cache_size_mb: 最大缓存大小（MB）
            cache_ttl_hours: 缓存有效期（小时）
            enable_cache: 是否启用缓存
        """
        self.enable_cache = enable_cache
        self.max_cache_size_mb = max_cache_size_mb
        self.cache_ttl = timedelta(hours=cache_ttl_hours)
        
        # 设置缓存目录
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            # 默认缓存目录
            self.cache_dir = Path(__file__).parent.parent.parent / "data" / "deepseek_cache"
        
        # 确保缓存目录存在
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 内存缓存（用于快速访问最近使用的缓存）
        self._memory_cache: Dict[str, Dict] = {}
        self._memory_cache_lock = threading.Lock()
        self._max_memory_cache_items = 100
        
        # 统计信息
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "total_requests": 0
        }
        self._stats_lock = threading.Lock()
        
        logger.info(f"DeepSeek缓存初始化完成，缓存目录: {self.cache_dir}")
    
    def _generate_cache_key(self, content: str, model: str = "deepseek-chat") -> str:
        """
        生成缓存键（基于内容哈希）
        
        Args:
            content: 文档内容
            model: 使用的模型名称
            
        Returns:
            缓存键字符串
        """
        # 使用 SHA256 哈希内容
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()[:32]
        # 组合模型名称生成唯一键
        return f"deepseek_{model}_{content_hash}"
    
    def _get_cache_file_path(self, cache_key: str) -> Path:
        """获取缓存文件路径"""
        return self.cache_dir / f"{cache_key}.cache"
    
    def _is_cache_valid(self, cache_data: Dict) -> bool:
        """
        检查缓存是否有效
        
        Args:
            cache_data: 缓存数据
            
        Returns:
            是否有效
        """
        if not cache_data:
            return False
        
        cached_at = cache_data.get("cached_at")
        if not cached_at:
            return False
        
        # 检查是否过期
        cached_time = datetime.fromisoformat(cached_at)
        return datetime.now() - cached_time < self.cache_ttl
    
    def get(self, content: str, model: str = "deepseek-chat") -> Optional[Dict]:
        """
        从缓存获取响应
        
        Args:
            content: 文档内容
            model: 使用的模型名称
            
        Returns:
            缓存的响应数据，如果不存在或已过期则返回 None
        """
        if not self.enable_cache:
            return None
        
        self._update_stats("total_requests")
        cache_key = self._generate_cache_key(content, model)
        
        # 1. 先检查内存缓存
        with self._memory_cache_lock:
            if cache_key in self._memory_cache:
                cached_data = self._memory_cache[cache_key]
                if self._is_cache_valid(cached_data):
                    self._update_stats("hits")
                    logger.debug(f"内存缓存命中: {cache_key[:20]}...")
                    return cached_data.get("response")
        
        # 2. 检查磁盘缓存
        cache_file = self._get_cache_file_path(cache_key)
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                
                if self._is_cache_valid(cached_data):
                    self._update_stats("hits")
                    # 加载到内存缓存
                    self._add_to_memory_cache(cache_key, cached_data)
                    logger.debug(f"磁盘缓存命中: {cache_key[:20]}...")
                    return cached_data.get("response")
                else:
                    # 缓存过期，删除文件
                    cache_file.unlink()
                    logger.debug(f"缓存已过期，已删除: {cache_key[:20]}...")
            except Exception as e:
                logger.warning(f"读取缓存文件失败: {e}")
        
        self._update_stats("misses")
        return None
    
    def set(
        self,
        content: str,
        response: Dict,
        model: str = "deepseek-chat",
        metadata: Dict = None
    ) -> bool:
        """
        保存响应到缓存
        
        Args:
            content: 文档内容
            response: API 响应数据
            model: 使用的模型名称
            metadata: 额外的元数据
            
        Returns:
            是否保存成功
        """
        if not self.enable_cache:
            return False
        
        cache_key = self._generate_cache_key(content, model)
        
        cache_data = {
            "cache_key": cache_key,
            "cached_at": datetime.now().isoformat(),
            "model": model,
            "response": response,
            "metadata": metadata or {}
        }
        
        try:
            # 1. 保存到磁盘
            cache_file = self._get_cache_file_path(cache_key)
            with open(cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
            
            # 2. 保存到内存缓存
            self._add_to_memory_cache(cache_key, cache_data)
            
            logger.debug(f"缓存已保存: {cache_key[:20]}...")
            
            # 3. 检查缓存大小并清理
            self._check_and_clean_cache()
            
            return True
            
        except Exception as e:
            logger.error(f"保存缓存失败: {e}")
            return False
    
    def _add_to_memory_cache(self, cache_key: str, cache_data: Dict):
        """添加到内存缓存"""
        with self._memory_cache_lock:
            # 如果超过最大数量，删除最旧的
            if len(self._memory_cache) >= self._max_memory_cache_items:
                # 简单策略：删除第一个
                first_key = next(iter(self._memory_cache))
                del self._memory_cache[first_key]
            
            self._memory_cache[cache_key] = cache_data
    
    def _update_stats(self, stat_type: str):
        """更新统计信息"""
        with self._stats_lock:
            if stat_type in self._stats:
                self._stats[stat_type] += 1
    
    def _check_and_clean_cache(self):
        """检查缓存大小并清理过期缓存"""
        try:
            total_size = 0
            cache_files = list(self.cache_dir.glob("*.cache"))
            
            for cache_file in cache_files:
                total_size += cache_file.stat().st_size
            
            total_size_mb = total_size / (1024 * 1024)
            
            # 如果超过最大大小，清理过期缓存
            if total_size_mb > self.max_cache_size_mb:
                logger.info(f"缓存大小 {total_size_mb:.2f}MB 超过限制，开始清理...")
                self._clean_expired_cache()
                
        except Exception as e:
            logger.error(f"检查缓存大小失败: {e}")
    
    def _clean_expired_cache(self):
        """清理过期的缓存"""
        cleaned = 0
        cache_files = list(self.cache_dir.glob("*.cache"))
        
        for cache_file in cache_files:
            try:
                with open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                
                if not self._is_cache_valid(cached_data):
                    cache_file.unlink()
                    cleaned += 1
                    
            except Exception:
                # 如果读取失败，也删除
                cache_file.unlink()
                cleaned += 1
        
        if cleaned > 0:
            self._update_stats("evictions")
            logger.info(f"已清理 {cleaned} 个过期缓存文件")
    
    def clear_all(self):
        """清空所有缓存"""
        # 清空内存缓存
        with self._memory_cache_lock:
            self._memory_cache.clear()
        
        # 清空磁盘缓存
        cache_files = list(self.cache_dir.glob("*.cache"))
        for cache_file in cache_files:
            cache_file.unlink()
        
        logger.info("已清空所有缓存")
    
    def get_stats(self) -> Dict:
        """获取缓存统计信息"""
        with self._stats_lock:
            stats = self._stats.copy()
        
        # 计算命中率
        if stats["total_requests"] > 0:
            stats["hit_rate"] = stats["hits"] / stats["total_requests"]
        else:
            stats["hit_rate"] = 0.0
        
        # 添加缓存文件数量
        cache_files = list(self.cache_dir.glob("*.cache"))
        stats["cache_files_count"] = len(cache_files)
        
        # 添加内存缓存数量
        with self._memory_cache_lock:
            stats["memory_cache_count"] = len(self._memory_cache)
        
        return stats
    
    def get_cache_info(self, content: str, model: str = "deepseek-chat") -> Dict:
        """
        获取缓存信息
        
        Args:
            content: 文档内容
            model: 模型名称
            
        Returns:
            缓存信息字典
        """
        cache_key = self._generate_cache_key(content, model)
        cache_file = self._get_cache_file_path(cache_key)
        
        info = {
            "cache_key": cache_key,
            "exists": False,
            "valid": False,
            "cached_at": None,
            "size_bytes": 0
        }
        
        if cache_file.exists():
            info["exists"] = True
            info["size_bytes"] = cache_file.stat().st_size
            
            try:
                with open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                info["cached_at"] = cached_data.get("cached_at")
                info["valid"] = self._is_cache_valid(cached_data)
            except Exception:
                pass
        
        return info


# 全局缓存实例
_cache_instance: Optional[DeepSeekCache] = None
_cache_lock = threading.Lock()


def get_cache_instance() -> DeepSeekCache:
    """获取全局缓存实例"""
    global _cache_instance
    
    if _cache_instance is None:
        with _cache_lock:
            if _cache_instance is None:
                _cache_instance = DeepSeekCache()
    
    return _cache_instance


def reset_cache_instance():
    """重置缓存实例（用于测试）"""
    global _cache_instance
    with _cache_lock:
        _cache_instance = None
