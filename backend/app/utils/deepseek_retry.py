#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek API 重试机制模块
支持指数退避、断路器模式和智能重试策略
"""

import time
import logging
import random
import threading
from typing import Callable, Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import wraps
from enum import Enum

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """断路器状态"""
    CLOSED = "closed"      # 正常状态，允许请求
    OPEN = "open"          # 断开状态，拒绝请求
    HALF_OPEN = "half_open"  # 半开状态，允许部分请求测试


@dataclass
class RetryStats:
    """重试统计信息"""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    retries: int = 0
    circuit_opens: int = 0
    last_failure_time: Optional[datetime] = None
    last_failure_reason: Optional[str] = None
    consecutive_failures: int = 0


@dataclass
class RetryConfig:
    """重试配置"""
    max_retries: int = 3
    base_delay: float = 1.0  # 基础延迟（秒）
    max_delay: float = 60.0  # 最大延迟（秒）
    exponential_base: float = 2.0  # 指数退避基数
    jitter: bool = True  # 是否添加随机抖动
    jitter_factor: float = 0.1  # 抖动因子
    
    # 断路器配置
    circuit_breaker_enabled: bool = True
    circuit_failure_threshold: int = 5  # 连续失败次数阈值
    circuit_recovery_timeout: int = 60  # 断路器恢复超时（秒）
    circuit_half_open_max_calls: int = 3  # 半开状态最大测试调用次数
    
    # 重试条件
    retry_on_timeout: bool = True
    retry_on_rate_limit: bool = True
    retry_on_server_error: bool = True
    retry_on_network_error: bool = True
    
    # 超时配置
    request_timeout: int = 60  # 请求超时（秒）


class CircuitBreaker:
    """断路器实现"""
    
    def __init__(self, config: RetryConfig):
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.half_open_calls = 0
        self._lock = threading.Lock()
    
    def is_allowed(self) -> bool:
        """检查是否允许请求"""
        with self._lock:
            if self.state == CircuitState.CLOSED:
                return True
            
            elif self.state == CircuitState.OPEN:
                # 检查是否可以进入半开状态
                if self._should_attempt_recovery():
                    self.state = CircuitState.HALF_OPEN
                    self.half_open_calls = 0
                    logger.info("断路器进入半开状态，开始测试恢复")
                    return True
                return False
            
            elif self.state == CircuitState.HALF_OPEN:
                # 半开状态下限制请求数量
                if self.half_open_calls < self.config.circuit_half_open_max_calls:
                    self.half_open_calls += 1
                    return True
                return False
        
        return False
    
    def _should_attempt_recovery(self) -> bool:
        """是否应该尝试恢复"""
        if self.last_failure_time is None:
            return True
        
        elapsed = datetime.now() - self.last_failure_time
        return elapsed.total_seconds() >= self.config.circuit_recovery_timeout
    
    def record_success(self):
        """记录成功请求"""
        with self._lock:
            self.failure_count = 0
            
            if self.state == CircuitState.HALF_OPEN:
                logger.info("断路器恢复正常状态")
                self.state = CircuitState.CLOSED
    
    def record_failure(self, reason: str = ""):
        """记录失败请求"""
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.state == CircuitState.HALF_OPEN:
                logger.warning(f"断路器半开状态下请求失败: {reason}，重新断开")
                self.state = CircuitState.OPEN
            
            elif self.state == CircuitState.CLOSED:
                if self.failure_count >= self.config.circuit_failure_threshold:
                    logger.warning(
                        f"连续失败 {self.failure_count} 次，断路器断开: {reason}"
                    )
                    self.state = CircuitState.OPEN
    
    def get_state(self) -> CircuitState:
        """获取当前状态"""
        with self._lock:
            return self.state


class DeepSeekRetry:
    """DeepSeek API 重试机制"""
    
    def __init__(self, config: RetryConfig = None):
        self.config = config or RetryConfig()
        self.circuit_breaker = CircuitBreaker(self.config)
        self.stats = RetryStats()
        self._stats_lock = threading.Lock()
    
    def _update_stats_success(self):
        """更新成功统计"""
        with self._stats_lock:
            self.stats.total_calls += 1
            self.stats.successful_calls += 1
            self.stats.consecutive_failures = 0
    
    def _update_stats_failure(self, reason: str):
        """更新失败统计"""
        with self._stats_lock:
            self.stats.total_calls += 1
            self.stats.failed_calls += 1
            self.stats.last_failure_time = datetime.now()
            self.stats.last_failure_reason = reason
            self.stats.consecutive_failures += 1
    
    def _update_stats_retry(self):
        """更新重试统计"""
        with self._stats_lock:
            self.stats.retries += 1
    
    def _update_stats_circuit_open(self):
        """更新断路器断开统计"""
        with self._stats_lock:
            self.stats.circuit_opens += 1
    
    def _calculate_delay(self, attempt: int) -> float:
        """
        计算重试延迟（指数退避 + 抖动）
        
        Args:
            attempt: 当前尝试次数
            
        Returns:
            延迟时间（秒）
        """
        # 指数退避
        delay = self.config.base_delay * (self.config.exponential_base ** (attempt - 1))
        
        # 限制最大延迟
        delay = min(delay, self.config.max_delay)
        
        # 添加随机抖动
        if self.config.jitter:
            jitter = delay * self.config.jitter_factor * random.random()
            delay = delay + jitter
        
        return delay
    
    def _should_retry(self, exception: Exception) -> bool:
        """
        判断是否应该重试
        
        Args:
            exception: 发生的异常
            
        Returns:
            是否应该重试
        """
        exception_str = str(exception).lower()
        exception_type = type(exception).__name__
        
        # 超时错误
        if self.config.retry_on_timeout:
            if 'timeout' in exception_str or exception_type == 'Timeout':
                return True
        
        # 速率限制
        if self.config.retry_on_rate_limit:
            if 'rate' in exception_str or '429' in exception_str:
                return True
        
        # 服务器错误 (5xx)
        if self.config.retry_on_server_error:
            if any(code in exception_str for code in ['500', '502', '503', '504']):
                return True
        
        # 网络错误
        if self.config.retry_on_network_error:
            network_errors = ['connection', 'network', 'dns', 'socket', 'refused']
            if any(err in exception_str for err in network_errors):
                return True
        
        return False
    
    def execute_with_retry(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        执行函数并自动重试
        
        Args:
            func: 要执行的函数
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            函数执行结果
            
        Raises:
            Exception: 所有重试失败后抛出最后一次异常
        """
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            # 检查断路器状态
            if self.config.circuit_breaker_enabled:
                if not self.circuit_breaker.is_allowed():
                    self._update_stats_circuit_open()
                    raise Exception(
                        f"断路器已断开，拒绝请求。"
                        f"连续失败: {self.stats.consecutive_failures}"
                    )
            
            try:
                result = func(*args, **kwargs)
                
                # 成功
                self.circuit_breaker.record_success()
                self._update_stats_success()
                
                return result
                
            except Exception as e:
                last_exception = e
                
                # 记录失败
                self.circuit_breaker.record_failure(str(e))
                self._update_stats_failure(str(e))
                
                # 判断是否应该重试
                if attempt < self.config.max_retries and self._should_retry(e):
                    # 计算延迟
                    delay = self._calculate_delay(attempt + 1)
                    
                    logger.warning(
                        f"DeepSeek API 调用失败 (尝试 {attempt + 1}/{self.config.max_retries + 1}): "
                        f"{type(e).__name__}: {e}. "
                        f"将在 {delay:.2f} 秒后重试..."
                    )
                    
                    self._update_stats_retry()
                    time.sleep(delay)
                else:
                    # 不再重试
                    break
        
        # 所有重试都失败
        logger.error(
            f"DeepSeek API 调用最终失败，已重试 {self.config.max_retries} 次: "
            f"{type(last_exception).__name__}: {last_exception}"
        )
        raise last_exception
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        with self._stats_lock:
            stats_dict = {
                "total_calls": self.stats.total_calls,
                "successful_calls": self.stats.successful_calls,
                "failed_calls": self.stats.failed_calls,
                "retries": self.stats.retries,
                "circuit_opens": self.stats.circuit_opens,
                "consecutive_failures": self.stats.consecutive_failures,
                "circuit_state": self.circuit_breaker.get_state().value,
                "last_failure_time": (
                    self.stats.last_failure_time.isoformat() 
                    if self.stats.last_failure_time else None
                ),
                "last_failure_reason": self.stats.last_failure_reason
            }
            
            # 计算成功率
            if stats_dict["total_calls"] > 0:
                stats_dict["success_rate"] = (
                    stats_dict["successful_calls"] / stats_dict["total_calls"]
                )
            else:
                stats_dict["success_rate"] = 1.0
            
            return stats_dict
    
    def reset_stats(self):
        """重置统计信息"""
        with self._stats_lock:
            self.stats = RetryStats()
    
    def reset_circuit_breaker(self):
        """重置断路器"""
        with self.circuit_breaker._lock:
            self.circuit_breaker.state = CircuitState.CLOSED
            self.circuit_breaker.failure_count = 0
            self.circuit_breaker.half_open_calls = 0
        logger.info("断路器已手动重置")


def with_retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    **retry_kwargs
):
    """
    重试装饰器
    
    Args:
        max_retries: 最大重试次数
        base_delay: 基础延迟
        **retry_kwargs: 其他重试配置
        
    Returns:
        装饰器函数
    """
    config = RetryConfig(
        max_retries=max_retries,
        base_delay=base_delay,
        **retry_kwargs
    )
    retry_handler = DeepSeekRetry(config)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return retry_handler.execute_with_retry(func, *args, **kwargs)
        
        # 附加重试处理器到函数
        wrapper.retry_handler = retry_handler
        return wrapper
    
    return decorator


# 全局重试实例
_retry_instance: Optional[DeepSeekRetry] = None
_retry_lock = threading.Lock()


def get_retry_instance(config: RetryConfig = None) -> DeepSeekRetry:
    """获取全局重试实例"""
    global _retry_instance
    
    if _retry_instance is None:
        with _retry_lock:
            if _retry_instance is None:
                _retry_instance = DeepSeekRetry(config)
    
    return _retry_instance


def reset_retry_instance():
    """重置重试实例（用于测试）"""
    global _retry_instance
    with _retry_lock:
        _retry_instance = None
