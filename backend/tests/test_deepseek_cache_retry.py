#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek 缓存和重试机制单元测试
"""

import pytest
import tempfile
import os
import time
from pathlib import Path

# 添加项目路径 - 必须在导入 app 之前
import sys
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# 现在可以导入 app 模块
from app.utils.deepseek_cache import DeepSeekCache, reset_cache_instance
from app.utils.deepseek_retry import (
    DeepSeekRetry, RetryConfig, CircuitState, 
    reset_retry_instance, with_retry
)


class TestDeepSeekCache:
    """测试 DeepSeek 缓存功能"""
    
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        """每个测试前重置缓存实例"""
        reset_cache_instance()
        self.cache_dir = tmp_path / "test_cache"
        self.cache = DeepSeekCache(
            cache_dir=str(self.cache_dir),
            max_cache_size_mb=10,
            cache_ttl_hours=1,
            enable_cache=True
        )
    
    def test_cache_set_and_get(self):
        """测试缓存存取"""
        content = "这是一段测试内容，用于测试缓存功能。"
        response = {
            "abstract": "测试摘要",
            "keywords": ["测试", "缓存"],
            "confidence_score": 0.9
        }
        
        # 设置缓存
        result = self.cache.set(content, response)
        assert result is True
        
        # 获取缓存
        cached = self.cache.get(content)
        assert cached is not None
        assert cached["abstract"] == "测试摘要"
        assert "测试" in cached["keywords"]
    
    def test_cache_miss(self):
        """测试缓存未命中"""
        content = "这是一段不存在于缓存中的内容。"
        cached = self.cache.get(content)
        assert cached is None
    
    def test_cache_key_consistency(self):
        """测试缓存键一致性"""
        content = "相同内容应该生成相同的缓存键"
        response1 = {"data": "value1"}
        response2 = {"data": "value2"}
        
        # 第一次设置
        self.cache.set(content, response1)
        cached1 = self.cache.get(content)
        
        # 第二次设置（覆盖）
        self.cache.set(content, response2)
        cached2 = self.cache.get(content)
        
        # 应该返回最新值
        assert cached2["data"] == "value2"
    
    def test_cache_disabled(self, tmp_path):
        """测试禁用缓存"""
        cache = DeepSeekCache(
            cache_dir=str(tmp_path / "disabled_cache"),
            enable_cache=False
        )
        
        content = "测试内容"
        response = {"data": "value"}
        
        # 设置缓存（应该不生效）
        cache.set(content, response)
        cached = cache.get(content)
        assert cached is None
    
    def test_cache_stats(self):
        """测试缓存统计"""
        content = "测试统计的内容"
        response = {"data": "value"}
        
        # 设置缓存
        self.cache.set(content, response)
        
        # 命中
        self.cache.get(content)
        
        # 未命中
        self.cache.get("不存在的内容")
        
        stats = self.cache.get_stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["total_requests"] == 2
        assert stats["hit_rate"] == 0.5
    
    def test_cache_clear(self):
        """测试清空缓存"""
        content = "测试清空的内容"
        response = {"data": "value"}
        
        self.cache.set(content, response)
        assert self.cache.get(content) is not None
        
        # 清空缓存
        self.cache.clear_all()
        assert self.cache.get(content) is None
    
    def test_cache_info(self):
        """测试缓存信息查询"""
        content = "测试信息查询的内容"
        response = {"data": "value"}
        
        # 设置前
        info_before = self.cache.get_cache_info(content)
        assert info_before["exists"] is False
        
        # 设置后
        self.cache.set(content, response)
        info_after = self.cache.get_cache_info(content)
        assert info_after["exists"] is True
        assert info_after["valid"] is True
        assert info_after["cached_at"] is not None


class TestDeepSeekRetry:
    """测试 DeepSeek 重试机制"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """每个测试前重置重试实例"""
        reset_retry_instance()
        self.config = RetryConfig(
            max_retries=3,
            base_delay=0.1,  # 测试时使用较短延迟
            max_delay=1.0,
            exponential_base=2.0,
            jitter=False,  # 测试时禁用抖动
            circuit_breaker_enabled=True,
            circuit_failure_threshold=3,
            circuit_recovery_timeout=1  # 测试时使用较短超时
        )
        self.retry = DeepSeekRetry(self.config)
    
    def test_successful_call(self):
        """测试成功调用"""
        def success_func():
            return {"result": "success"}
        
        result = self.retry.execute_with_retry(success_func)
        assert result["result"] == "success"
        
        stats = self.retry.get_stats()
        assert stats["successful_calls"] == 1
        assert stats["total_calls"] == 1
    
    def test_retry_on_failure(self):
        """测试失败重试"""
        call_count = [0]
        
        def failing_func():
            call_count[0] += 1
            if call_count[0] < 3:
                raise ConnectionError("Connection refused")
            return {"result": "success after retry"}
        
        result = self.retry.execute_with_retry(failing_func)
        assert result["result"] == "success after retry"
        assert call_count[0] == 3
        
        stats = self.retry.get_stats()
        assert stats["retries"] == 2
        assert stats["successful_calls"] == 1
    
    def test_max_retries_exceeded(self):
        """测试超过最大重试次数"""
        # 使用独立的重试实例，禁用断路器以测试纯重试逻辑
        config = RetryConfig(
            max_retries=3,
            base_delay=0.1,
            max_delay=1.0,
            circuit_breaker_enabled=False
        )
        retry = DeepSeekRetry(config)
        
        def always_fail():
            raise TimeoutError("Request timeout")
        
        with pytest.raises(TimeoutError):
            retry.execute_with_retry(always_fail)
        
        stats = retry.get_stats()
        # failed_calls 记录的是所有失败次数（包括重试）
        # 初始调用 + 3次重试 = 4次失败
        assert stats["failed_calls"] == 4
        assert stats["retries"] == 3
    
    def test_circuit_breaker_open(self):
        """测试断路器打开"""
        call_count = [0]
        
        def always_fail():
            call_count[0] += 1
            raise Exception("Server error 500")
        
        # 触发断路器
        for _ in range(5):
            try:
                self.retry.execute_with_retry(always_fail)
            except:
                pass
        
        # 断路器应该已打开
        assert self.retry.circuit_breaker.state == CircuitState.OPEN
        
        # 再次调用应该被拒绝
        with pytest.raises(Exception, match="断路器已断开"):
            self.retry.execute_with_retry(always_fail)
    
    def test_circuit_breaker_recovery(self):
        """测试断路器恢复"""
        call_count = [0]
        
        def failing_func():
            call_count[0] += 1
            if call_count[0] < 4:
                raise Exception("Temporary error")
            return {"result": "success"}
        
        # 触发断路器
        for _ in range(3):
            try:
                self.retry.execute_with_retry(failing_func)
            except:
                pass
        
        assert self.retry.circuit_breaker.state == CircuitState.OPEN
        
        # 等待恢复超时
        time.sleep(1.5)
        
        # 断路器应该允许测试请求
        call_count[0] = 3  # 重置计数，下次调用会成功
        result = self.retry.execute_with_retry(failing_func)
        assert result["result"] == "success"
    
    def test_retry_decorator(self):
        """测试重试装饰器"""
        call_count = [0]
        
        @with_retry(max_retries=2, base_delay=0.1)
        def decorated_func():
            call_count[0] += 1
            if call_count[0] < 2:
                raise ConnectionError("Connection error")
            return "success"
        
        result = decorated_func()
        assert result == "success"
        assert call_count[0] == 2
    
    def test_retry_stats(self):
        """测试重试统计"""
        def success_func():
            return "ok"
        
        def fail_func():
            raise Exception("error")
        
        # 成功调用
        self.retry.execute_with_retry(success_func)
        
        # 失败调用
        try:
            self.retry.execute_with_retry(fail_func)
        except:
            pass
        
        stats = self.retry.get_stats()
        assert stats["total_calls"] == 2
        assert stats["successful_calls"] == 1
        assert stats["failed_calls"] == 1
        assert "success_rate" in stats
    
    def test_exponential_backoff(self):
        """测试指数退避延迟计算"""
        delays = []
        for attempt in range(1, 4):
            delay = self.retry._calculate_delay(attempt)
            delays.append(delay)
        
        # 验证指数增长
        assert delays[1] > delays[0]
        assert delays[2] > delays[1]
        
        # 验证不超过最大延迟
        for delay in delays:
            assert delay <= self.config.max_delay


class TestIntegration:
    """集成测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        """设置测试环境"""
        reset_cache_instance()
        reset_retry_instance()
        
        self.cache_dir = tmp_path / "integration_cache"
        self.cache = DeepSeekCache(
            cache_dir=str(self.cache_dir),
            enable_cache=True
        )
        
        self.config = RetryConfig(
            max_retries=2,
            base_delay=0.1,
            circuit_breaker_enabled=False,  # 简化测试
            retry_on_network_error=True  # 启用网络错误重试
        )
        self.retry = DeepSeekRetry(self.config)
    
    def test_cache_with_retry_integration(self):
        """测试缓存与重试的集成"""
        content = "集成测试内容"
        expected_response = {"abstract": "集成测试摘要"}
        
        api_call_count = [0]
        
        def mock_api_call():
            api_call_count[0] += 1
            if api_call_count[0] < 2:
                # 使用包含 "connection" 的错误消息，以触发网络错误重试
                raise ConnectionError("Connection refused")
            return expected_response
        
        # 第一次调用（会重试）
        result1 = self.retry.execute_with_retry(mock_api_call)
        self.cache.set(content, result1)
        
        # 第二次调用（从缓存获取，不需要调用 API）
        cached_result = self.cache.get(content)
        
        assert cached_result == expected_response
        assert api_call_count[0] == 2  # 第一次调用有1次重试


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
